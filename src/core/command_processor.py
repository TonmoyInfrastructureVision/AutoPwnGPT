#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command Processor for AutoPwnGPT.
Processes natural language commands into structured module operations.
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from src.llm_integration.llm_manager import LlmManager


class CommandProcessor:
    """
    Processes natural language commands into structured module operations.
    Uses LLM to understand intent and extract parameters.
    """
    
    def __init__(self, config: Dict[str, Any], llm_manager: LlmManager = None):
        """
        Initialize the command processor.
        
        Args:
            config: Configuration dictionary.
            llm_manager: LLM manager instance.
        """
        self.logger = logging.getLogger("autopwngpt.core.command_processor")
        self.config = config
        self.llm_manager = llm_manager or LlmManager(config)
        
        # Keep track of command history
        self.command_history = []
        
        # Command patterns for direct command matching (without LLM)
        self.direct_patterns = {
            r"^scan\s+(\S+)(\s+.*)?$": self._handle_scan_command,
            r"^help(\s+.*)?$": self._handle_help_command,
            r"^list\s+modules(\s+.*)?$": self._handle_list_modules_command,
            r"^clear\s+context$": self._handle_clear_context_command,
            r"^exit$|^quit$": self._handle_exit_command,
        }
    
    async def process_command(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a natural language command.
        
        Args:
            command: The natural language command.
            context: The current context.
            
        Returns:
            A dictionary containing the processed command information.
        """
        self.logger.debug(f"Processing command: {command}")
        self.command_history.append(command)
        
        # Check for direct command patterns first
        for pattern, handler in self.direct_patterns.items():
            match = re.match(pattern, command, re.IGNORECASE)
            if match:
                return handler(*match.groups(), context=context)
        
        # Use LLM for complex command parsing
        return await self._process_with_llm(command, context)
    
    async def _process_with_llm(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a command using the LLM.
        
        Args:
            command: The natural language command.
            context: The current context.
            
        Returns:
            A dictionary containing the processed command information.
        """
        try:
            # Build prompt with command and context
            prompt = self._build_command_prompt(command, context)
            
            # Get response from LLM
            llm_response = await self.llm_manager.generate_response(prompt)
            
            # Parse response
            parsed_response = self._parse_llm_response(llm_response)
            
            if not parsed_response:
                return {
                    "success": False,
                    "error": "Could not parse LLM response",
                    "original_command": command,
                    "raw_response": llm_response
                }
            
            return {
                "success": True,
                "original_command": command,
                "module": parsed_response.get("module"),
                "args": parsed_response.get("args", {}),
                "description": parsed_response.get("description", ""),
                "confidence": parsed_response.get("confidence", 0.0),
                "raw_response": llm_response
            }
            
        except Exception as e:
            self.logger.exception(f"Error processing command with LLM: {str(e)}")
            return {
                "success": False,
                "error": f"Error processing command: {str(e)}",
                "original_command": command
            }
    
    def _build_command_prompt(self, command: str, context: Dict[str, Any] = None) -> str:
        """
        Build a prompt for the LLM to process a command.
        
        Args:
            command: The natural language command.
            context: The current context.
            
        Returns:
            The prompt string.
        """
        # Start with the system prompt
        prompt = """You are AutoPwnGPT, an offensive security assistant. Your task is to translate natural language security commands into specific module operations.

Given a user's command, you must identify:
1. Which module should be executed
2. What arguments should be passed to the module
3. A brief description of what the command is trying to do

Respond with a JSON object containing:
- "module": the name of the module to execute
- "args": an object containing arguments for the module
- "description": a brief description of the operation
- "confidence": a number from 0 to 1 indicating your confidence in the interpretation

Available modules:
- PortScanner: Scans network ports (args: target, ports)
- NetworkScanner: Discovers hosts on a network (args: network)
- WebScanner: Scans web applications (args: url, depth)
- VulnerabilityScanner: Scans for vulnerabilities (args: target, scan_type)
- SqlInjection: Tests for SQL injection (args: url, parameters)
- XssExploit: Tests for XSS vulnerabilities (args: url, parameters)
- DirectoryEnumerator: Enumerates directories (args: url, wordlist)
- CredentialBruteForce: Brute forces authentication (args: target, service, wordlist)

"""
        
        # Add context summary if available
        if context:
            targets = context.get("targets", {})
            findings = context.get("findings", {})
            
            if targets:
                prompt += "\nCurrent targets:\n"
                for target_id, target_data in targets.items():
                    prompt += f"- {target_id}: {target_data.get('type', 'unknown')} ({target_data.get('address', 'unknown')})\n"
            
            if findings:
                prompt += "\nRecent findings:\n"
                recent_findings = list(findings.items())[-5:]  # Last 5 findings
                for finding_id, finding_data in recent_findings:
                    prompt += f"- {finding_data.get('title', 'unknown finding')}\n"
        
        # Add command history for context
        if len(self.command_history) > 1:  # If there's more than just the current command
            prompt += "\nRecent commands:\n"
            for cmd in self.command_history[-6:-1]:  # Last 5 commands excluding current
                prompt += f"- {cmd}\n"
        
        # Add the current command
        prompt += f"\nUser command: {command}\n\nParsed command:"
        
        return prompt
    
    def _parse_llm_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse the LLM response to extract structured command data.
        
        Args:
            response: The LLM response string.
            
        Returns:
            A dictionary containing the parsed command information, or None if parsing failed.
        """
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                # Extract JSON from code block
                json_str = json_match.group(1)
            else:
                # Try to find JSON without code blocks
                json_match = re.search(r'(\{.*\})', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    self.logger.warning("Could not find JSON in LLM response")
                    return None
            
            # Parse JSON
            parsed = json.loads(json_str)
            return parsed
            
        except Exception as e:
            self.logger.error(f"Error parsing LLM response: {str(e)}")
            return None
    
    def _handle_scan_command(self, target: str, options: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle a direct scan command.
        
        Args:
            target: The target to scan.
            options: Additional options for the scan.
            context: The current context.
            
        Returns:
            A dictionary containing the processed command information.
        """
        # Remove leading/trailing whitespace
        target = target.strip()
        options_dict = {}
        
        # Parse options if provided
        if options:
            options = options.strip()
            # Example: -p 80,443 -sV
            port_match = re.search(r'-p\s+([0-9,-]+)', options)
            if port_match:
                options_dict["ports"] = port_match.group(1)
            
            # Extract scan type
            if "-sV" in options:
                options_dict["service_detection"] = True
            if "-sC" in options:
                options_dict["script_scan"] = True
        
        # Determine scan type based on target format
        if re.match(r'^https?://', target):
            module = "WebScanner"
            args = {"url": target, **options_dict}
        elif re.match(r'^\d+\.\d+\.\d+\.\d+(/\d+)?$', target) or re.match(r'^\d+\.\d+\.\d+\.\d+-\d+$', target):
            module = "NetworkScanner"
            args = {"network": target, **options_dict}
        else:
            module = "PortScanner"
            args = {"target": target, **options_dict}
        
        return {
            "success": True,
            "original_command": f"scan {target}{' ' + options if options else ''}",
            "module": module,
            "args": args,
            "description": f"Scanning {target}",
            "confidence": 1.0
        }
    
    def _handle_help_command(self, topic: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle a help command.
        
        Args:
            topic: The help topic.
            context: The current context.
            
        Returns:
            A dictionary containing the processed command information.
        """
        topic = (topic or "").strip()
        
        return {
            "success": True,
            "original_command": f"help{' ' + topic if topic else ''}",
            "module": "HelpCommand",
            "args": {"topic": topic if topic else "general"},
            "description": f"Displaying help{' for ' + topic if topic else ''}",
            "confidence": 1.0
        }
    
    def _handle_list_modules_command(self, category: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle a list modules command.
        
        Args:
            category: The module category to list.
            context: The current context.
            
        Returns:
            A dictionary containing the processed command information.
        """
        category = (category or "").strip()
        
        return {
            "success": True,
            "original_command": f"list modules{' ' + category if category else ''}",
            "module": "ListModules",
            "args": {"category": category if category else "all"},
            "description": f"Listing {'all modules' if not category else f'{category} modules'}",
            "confidence": 1.0
        }
    
    def _handle_clear_context_command(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle a clear context command.
        
        Args:
            context: The current context.
            
        Returns:
            A dictionary containing the processed command information.
        """
        return {
            "success": True,
            "original_command": "clear context",
            "module": "ClearContext",
            "args": {},
            "description": "Clearing session context",
            "confidence": 1.0
        }
    
    def _handle_exit_command(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle an exit command.
        
        Args:
            context: The current context.
            
        Returns:
            A dictionary containing the processed command information.
        """
        return {
            "success": True,
            "original_command": "exit",
            "module": "Exit",
            "args": {},
            "description": "Exiting application",
            "confidence": 1.0
        }
