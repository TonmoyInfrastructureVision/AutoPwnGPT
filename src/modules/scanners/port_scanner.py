#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Port Scanner Module for AutoPwnGPT.
Uses nmap to scan for open ports on target systems.
"""

import asyncio
import ipaddress
import json
import logging
import os
import re
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from src.modules.base_module import BaseModule, ModuleResult, ModuleFinding, ModuleSeverity


class PortScanner(BaseModule):
    """
    Port scanner module using nmap.
    Scans target hosts for open ports and services.
    """
    
    def __init__(self, context: Dict[str, Any] = None):
        """Initialize the port scanner module."""
        super().__init__(context)
        self.name = "PortScanner"
        self.description = "Scans target hosts for open ports and services using nmap"
        self.version = "1.0.0"
        
        # Module-specific parameters
        self.required_args = ["target"]
        self.optional_args = {
            "ports": "Ports to scan, comma-separated (default: top 1000)",
            "speed": "Scan speed (1-5, where 5 is fastest, default: 3)",
            "service_detection": "Enable service version detection (default: False)",
            "script_scan": "Enable default script scanning (default: False)",
            "output_format": "Output format (json, text, default: json)",
            "timeout": "Scan timeout in seconds (default: 300)"
        }
        
        # Validate nmap is installed
        self._check_nmap_installed()
    
    def _check_nmap_installed(self) -> None:
        """Check if nmap is installed on the system."""
        try:
            result = subprocess.run(
                ["nmap", "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                check=False
            )
            if result.returncode != 0:
                self.logger.warning("nmap is not installed or not in PATH")
            else:
                self.logger.debug(f"Found nmap: {result.stdout.splitlines()[0] if result.stdout else 'Unknown version'}")
        except Exception as e:
            self.logger.warning(f"Error checking nmap installation: {str(e)}")
    
    async def _execute(self, args: Dict[str, Any]) -> ModuleResult:
        """
        Execute the port scan.
        
        Args:
            args: Arguments for the scan.
                target: Target to scan (IP, hostname, or CIDR notation)
                ports: Ports to scan, comma-separated (optional)
                speed: Scan speed (1-5, where 5 is fastest, optional)
                service_detection: Enable service version detection (optional)
                script_scan: Enable default script scanning (optional)
                output_format: Output format (json, text, optional)
                timeout: Scan timeout in seconds (optional)
                
        Returns:
            The scan result.
        """
        target = args.get("target")
        ports = args.get("ports", "")
        speed = int(args.get("speed", 3))
        service_detection = args.get("service_detection", False)
        script_scan = args.get("script_scan", False)
        output_format = args.get("output_format", "json")
        timeout = int(args.get("timeout", 300))
        
        # Validate target
        if not self._is_valid_target(target):
            return ModuleResult(
                success=False,
                error_message=f"Invalid target: {target}"
            )
        
        # Build nmap command
        cmd = ["nmap", "-T", str(speed)]
        
        # Add ports if specified
        if ports:
            cmd.extend(["-p", ports])
        
        # Add service detection if enabled
        if service_detection:
            cmd.append("-sV")
        
        # Add script scanning if enabled
        if script_scan:
            cmd.append("-sC")
        
        # Add XML output for parsing
        xml_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
        xml_file.close()
        cmd.extend(["-oX", xml_file.name])
        
        # Add target
        cmd.append(target)
        
        self.logger.info(f"Running nmap scan against {target}")
        self.logger.debug(f"Command: {' '.join(cmd)}")
        
        try:
            # Run nmap
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for nmap to complete with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return ModuleResult(
                    success=False,
                    error_message=f"Scan timed out after {timeout} seconds"
                )
            
            # Check if scan was successful
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                self.logger.error(f"nmap scan failed: {error_msg}")
                return ModuleResult(
                    success=False,
                    error_message=f"nmap scan failed: {error_msg}"
                )
            
            # Parse scan output
            result = self._parse_nmap_output(xml_file.name, output_format)
            
            # Create findings
            findings = self._create_findings(result)
            
            return ModuleResult(
                success=True,
                findings=findings,
                raw_output=result
            )
            
        except Exception as e:
            self.logger.exception(f"Error executing port scan: {str(e)}")
            return ModuleResult(
                success=False,
                error_message=f"Error executing port scan: {str(e)}"
            )
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(xml_file.name):
                    os.unlink(xml_file.name)
            except Exception as e:
                self.logger.warning(f"Error cleaning up temporary files: {str(e)}")
    
    def _is_valid_target(self, target: str) -> bool:
        """
        Check if a target is valid.
        
        Args:
            target: The target to validate.
            
        Returns:
            True if the target is valid, False otherwise.
        """
        # IP address (IPv4 or IPv6)
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            pass
        
        # CIDR notation
        try:
            ipaddress.ip_network(target, strict=False)
            return True
        except ValueError:
            pass
        
        # Hostname (basic validation)
        hostname_pattern = r'^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])(\.[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])*$'
        if re.match(hostname_pattern, target):
            return True
        
        return False
    
    def _parse_nmap_output(self, xml_file: str, output_format: str = "json") -> Dict[str, Any]:
        """
        Parse nmap XML output.
        
        Args:
            xml_file: Path to the XML output file.
            output_format: Output format (json, text).
            
        Returns:
            Parsed scan results.
        """
        try:
            # This is a simple implementation - in a real-world scenario,
            # you would use a library like python-libnmap for more robust parsing
            result = self._convert_xml_to_dict(xml_file)
            
            # Extract relevant information
            parsed_result = {
                "hosts": [],
                "scan_info": {
                    "start_time": result.get("nmaprun", {}).get("@start", ""),
                    "version": result.get("nmaprun", {}).get("@version", ""),
                    "args": result.get("nmaprun", {}).get("@args", "")
                }
            }
            
            # Parse host information
            hosts = result.get("nmaprun", {}).get("host", [])
            if not isinstance(hosts, list):
                hosts = [hosts]
            
            for host in hosts:
                host_info = {
                    "ip": self._get_address(host),
                    "hostnames": self._get_hostnames(host),
                    "status": self._get_status(host),
                    "ports": self._get_ports(host)
                }
                parsed_result["hosts"].append(host_info)
            
            return parsed_result
            
        except Exception as e:
            self.logger.error(f"Error parsing nmap output: {str(e)}")
            return {"error": f"Error parsing nmap output: {str(e)}"}
    
    def _convert_xml_to_dict(self, xml_file: str) -> Dict[str, Any]:
        """
        Convert XML to dictionary.
        
        Args:
            xml_file: Path to the XML file.
            
        Returns:
            Dictionary representation of the XML.
        """
        # In a real implementation, you would use a library like xmltodict
        # For simplicity, we'll use a mock result here
        import xml.etree.ElementTree as ET
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Convert XML to dictionary (simplified)
            result = {
                "nmaprun": {
                    "@version": root.get("version", ""),
                    "@args": root.get("args", ""),
                    "@start": root.get("start", ""),
                    "host": []
                }
            }
            
            # Parse host information
            for host_elem in root.findall(".//host"):
                host = {
                    "address": [],
                    "hostnames": [],
                    "ports": {"port": []}
                }
                
                # Address
                for addr in host_elem.findall(".//address"):
                    host["address"].append({
                        "@addr": addr.get("addr", ""),
                        "@addrtype": addr.get("addrtype", "")
                    })
                
                # Hostnames
                hostnames_elem = host_elem.find(".//hostnames")
                if hostnames_elem is not None:
                    for hostname in hostnames_elem.findall(".//hostname"):
                        host["hostnames"].append({
                            "@name": hostname.get("name", ""),
                            "@type": hostname.get("type", "")
                        })
                
                # Status
                status_elem = host_elem.find(".//status")
                if status_elem is not None:
                    host["status"] = {
                        "@state": status_elem.get("state", ""),
                        "@reason": status_elem.get("reason", "")
                    }
                
                # Ports
                ports_elem = host_elem.find(".//ports")
                if ports_elem is not None:
                    for port_elem in ports_elem.findall(".//port"):
                        port = {
                            "@protocol": port_elem.get("protocol", ""),
                            "@portid": port_elem.get("portid", "")
                        }
                        
                        # State
                        state_elem = port_elem.find(".//state")
                        if state_elem is not None:
                            port["state"] = {
                                "@state": state_elem.get("state", ""),
                                "@reason": state_elem.get("reason", "")
                            }
                        
                        # Service
                        service_elem = port_elem.find(".//service")
                        if service_elem is not None:
                            port["service"] = {
                                "@name": service_elem.get("name", ""),
                                "@product": service_elem.get("product", ""),
                                "@version": service_elem.get("version", ""),
                                "@ostype": service_elem.get("ostype", "")
                            }
                        
                        host["ports"]["port"].append(port)
                
                result["nmaprun"]["host"].append(host)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error converting XML to dictionary: {str(e)}")
            return {}
    
    def _get_address(self, host: Dict[str, Any]) -> str:
        """
        Get the IP address from a host dictionary.
        
        Args:
            host: Host dictionary.
            
        Returns:
            IP address.
        """
        addresses = host.get("address", [])
        if not isinstance(addresses, list):
            addresses = [addresses]
        
        for addr in addresses:
            if addr.get("@addrtype") == "ipv4":
                return addr.get("@addr", "")
        
        # If no IPv4 address, return the first address
        return addresses[0].get("@addr", "") if addresses else ""
    
    def _get_hostnames(self, host: Dict[str, Any]) -> List[str]:
        """
        Get hostnames from a host dictionary.
        
        Args:
            host: Host dictionary.
            
        Returns:
            List of hostnames.
        """
        hostnames = host.get("hostnames", [])
        if not isinstance(hostnames, list):
            hostnames = [hostnames]
        
        result = []
        for hostname in hostnames:
            name = hostname.get("@name", "")
            if name:
                result.append(name)
        
        return result
    
    def _get_status(self, host: Dict[str, Any]) -> str:
        """
        Get the status from a host dictionary.
        
        Args:
            host: Host dictionary.
            
        Returns:
            Host status.
        """
        status = host.get("status", {})
        return status.get("@state", "unknown")
    
    def _get_ports(self, host: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get ports from a host dictionary.
        
        Args:
            host: Host dictionary.
            
        Returns:
            List of port dictionaries.
        """
        ports = host.get("ports", {}).get("port", [])
        if not isinstance(ports, list):
            ports = [ports]
        
        result = []
        for port in ports:
            state = port.get("state", {}).get("@state", "")
            if state == "open":
                result.append({
                    "port": port.get("@portid", ""),
                    "protocol": port.get("@protocol", ""),
                    "service": port.get("service", {}).get("@name", ""),
                    "product": port.get("service", {}).get("@product", ""),
                    "version": port.get("service", {}).get("@version", "")
                })
        
        return result
    
    def _create_findings(self, scan_result: Dict[str, Any]) -> List[ModuleFinding]:
        """
        Create findings from scan results.
        
        Args:
            scan_result: Scan results.
            
        Returns:
            List of findings.
        """
        findings = []
        
        for host in scan_result.get("hosts", []):
            ip = host.get("ip", "")
            hostnames = host.get("hostnames", [])
            hostname = hostnames[0] if hostnames else ""
            
            # Create a finding for each open port
            for port in host.get("ports", []):
                port_num = port.get("port", "")
                protocol = port.get("protocol", "tcp")
                service = port.get("service", "")
                product = port.get("product", "")
                version = port.get("version", "")
                
                # Determine severity based on service
                severity = self._determine_severity(service, port_num)
                
                # Create finding title
                title = f"Open port {port_num}/{protocol}"
                if service:
                    title += f" ({service})"
                
                # Create finding description
                description = f"Open port {port_num}/{protocol} detected on {ip}"
                if hostname:
                    description += f" ({hostname})"
                if service:
                    description += f"\nService: {service}"
                if product:
                    description += f"\nProduct: {product}"
                if version:
                    description += f"\nVersion: {version}"
                
                # Create finding details
                details = {
                    "ip": ip,
                    "hostnames": hostnames,
                    "port": port_num,
                    "protocol": protocol,
                    "service": service,
                    "product": product,
                    "version": version
                }
                
                # Create remediation suggestion
                remediation = f"Review whether port {port_num}/{protocol} needs to be exposed."
                
                # Create finding
                finding = ModuleFinding(
                    title=title,
                    description=description,
                    severity=severity,
                    details=details,
                    remediation=remediation
                )
                
                findings.append(finding)
        
        return findings
    
    def _determine_severity(self, service: str, port: str) -> ModuleSeverity:
        """
        Determine the severity of a finding based on the service and port.
        
        Args:
            service: Service name.
            port: Port number.
            
        Returns:
            Severity level.
        """
        # High risk services
        high_risk_services = ["telnet", "ftp", "rsh", "rlogin", "rexec", "rcmd"]
        if service.lower() in high_risk_services:
            return ModuleSeverity.HIGH
        
        # Medium risk services
        medium_risk_services = ["ssh", "smtp", "dns", "http", "pop3", "imap", "snmp"]
        if service.lower() in medium_risk_services:
            return ModuleSeverity.MEDIUM
        
        # High risk ports
        high_risk_ports = ["21", "23", "512", "513", "514", "135", "139", "445", "3389"]
        if port in high_risk_ports:
            return ModuleSeverity.HIGH
        
        # Default severity
        return ModuleSeverity.LOW
