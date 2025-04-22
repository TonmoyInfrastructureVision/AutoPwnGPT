#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command Line Interface for AutoPwnGPT.
Provides an interactive console for interacting with the system.
"""

import asyncio
import json
import logging
import os
import readline
import shlex
import sys
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax


class CliInterface:
    """
    Command Line Interface for AutoPwnGPT.
    Provides an interactive console for interacting with the system.
    """
    
    def __init__(self, config: Dict[str, Any], engine: Any, command_processor: Any):
        """
        Initialize the CLI interface.
        
        Args:
            config: Configuration dictionary.
            engine: Engine instance.
            command_processor: CommandProcessor instance.
        """
        self.logger = logging.getLogger("autopwngpt.cli")
        self.config = config
        self.engine = engine
        self.command_processor = command_processor
        
        # Get CLI configuration
        cli_config = config.get("cli", {})
        self.prompt = cli_config.get("prompt_style", "autopwngpt> ")
        self.history_file = cli_config.get("history_file", ".autopwngpt_history")
        
        # Rich console for pretty output
        self.console = Console()
        
        # Command history
        self.history = []
        self.running = True
        
        # Load command history
        self._load_history()
    
    def _load_history(self) -> None:
        """Load command history from file."""
        try:
            # Set up readline history
            if os.path.exists(self.history_file):
                readline.read_history_file(self.history_file)
            
            self.logger.debug("Command history loaded")
        except Exception as e:
            self.logger.error(f"Error loading command history: {str(e)}")
    
    def _save_history(self) -> None:
        """Save command history to file."""
        try:
            # Make sure the directory exists
            os.makedirs(os.path.dirname(os.path.abspath(self.history_file)), exist_ok=True)
            
            # Save readline history
            readline.write_history_file(self.history_file)
            
            self.logger.debug("Command history saved")
        except Exception as e:
            self.logger.error(f"Error saving command history: {str(e)}")
    
    async def run(self) -> None:
        """Run the CLI interface."""
        self._display_welcome()
        
        # Main command loop
        self.running = True
        while self.running:
            try:
                # Get user input
                command = await self._get_input()
                
                # Skip empty commands
                if not command:
                    continue
                
                # Add command to history
                self.history.append(command)
                
                # Process the command
                await self._process_command(command)
                
            except KeyboardInterrupt:
                self.console.print("\nUse 'exit' or 'quit' to exit", style="yellow")
            except EOFError:
                self.running = False
                self.console.print("\nExiting...", style="yellow")
            except Exception as e:
                self.logger.exception(f"Error in CLI loop: {str(e)}")
                self.console.print(f"Error: {str(e)}", style="bold red")
        
        # Save command history before exiting
        self._save_history()
    
    async def _get_input(self) -> str:
        """
        Get user input.
        
        Returns:
            User input string.
        """
        # This is a blocking operation, but it's OK in this context
        # In a more complex application, we might use a non-blocking approach
        return input(self.prompt).strip()
    
    async def _process_command(self, command: str) -> None:
        """
        Process a command.
        
        Args:
            command: Command string.
        """
        # Handle built-in commands
        if command.lower() in ["exit", "quit"]:
            self.running = False
            self.console.print("Exiting...", style="yellow")
            return
        
        if command.lower() == "help":
            self._display_help()
            return
        
        if command.lower() == "version":
            self._display_version()
            return
        
        if command.lower() == "clear":
            os.system("cls" if sys.platform == "win32" else "clear")
            return
        
        if command.lower().startswith("save "):
            _, filename = command.split(" ", 1)
            self._save_session(filename)
            return
        
        if command.lower().startswith("load "):
            _, filename = command.split(" ", 1)
            self.load_session(filename)
            return
        
        if command.lower() == "modules":
            self._display_modules()
            return
        
        # Process command with command processor
        self.console.print(f"[cyan]Processing command:[/cyan] {command}")
        
        try:
            # Process command
            result = await self.command_processor.process_command(command, self.engine.get_context())
            
            # Check if command was processed successfully
            if result.get("success", False):
                module = result.get("module")
                args = result.get("args", {})
                description = result.get("description", "")
                
                if module == "Exit":
                    self.running = False
                    self.console.print("Exiting...", style="yellow")
                    return
                
                if module == "HelpCommand":
                    topic = args.get("topic", "general")
                    self._display_help(topic)
                    return
                
                if module == "ListModules":
                    category = args.get("category", "all")
                    self._display_modules(category)
                    return
                
                if module == "ClearContext":
                    self.engine.reset_context()
                    self.console.print("Context cleared", style="green")
                    return
                
                # Execute module
                self.console.print(f"[green]Executing:[/green] {description}")
                
                # Execute the module and get results
                task_id, result = await self.engine.execute_module(module, args)
                
                # Display results
                self._display_result(task_id, result)
                
            else:
                # Command processing failed
                error = result.get("error", "Unknown error")
                self.console.print(f"[bold red]Error:[/bold red] {error}")
                
                # If there's a raw response, print it for debugging
                if "raw_response" in result:
                    self.console.print("\n[dim]Raw response:[/dim]")
                    self.console.print(result["raw_response"], soft_wrap=True)
                
        except Exception as e:
            self.logger.exception(f"Error processing command: {str(e)}")
            self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    def _display_welcome(self) -> None:
        """Display welcome message."""
        welcome_text = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║               ╔═╗╦ ╦╔╦╗╔═╗╔═╗╦ ╦╔╗╔╔═╗╔═╗╔╦╗         ║
║               ╠═╣║ ║ ║ ║ ║╠═╝║║║║║║║ ╦╠═╝ ║          ║
║               ╩ ╩╚═╝ ╩ ╚═╝╩  ╚╩╝╝╚╝╚═╝╩   ╩          ║
║                                                      ║
║         Natural Language Penetration Testing         ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
        """
        self.console.print(welcome_text, style="bold blue")
        self.console.print("Type what you want to do — AutoPwnGPT will figure out how to do it.\n", style="italic")
        self.console.print("Type 'help' for a list of commands.", style="yellow")
    
    def _display_help(self, topic: str = "general") -> None:
        """
        Display help information.
        
        Args:
            topic: Help topic to display.
        """
        if topic == "general":
            # General help
            help_table = Table(title="AutoPwnGPT Commands")
            help_table.add_column("Command", style="cyan", no_wrap=True)
            help_table.add_column("Description", style="green")
            
            # Add built-in commands
            help_table.add_row("help [topic]", "Display help information")
            help_table.add_row("version", "Display version information")
            help_table.add_row("clear", "Clear the screen")
            help_table.add_row("save <filename>", "Save the current session")
            help_table.add_row("load <filename>", "Load a saved session")
            help_table.add_row("modules", "List available modules")
            help_table.add_row("exit, quit", "Exit the application")
            
            # Add common natural language commands
            help_table.add_row("scan <target>", "Scan a target for open ports")
            help_table.add_row("find vulnerabilities on <target>", "Find vulnerabilities on a target")
            help_table.add_row("test sql injection on <url>", "Test for SQL injection vulnerabilities")
            help_table.add_row("enumerate directories on <url>", "Enumerate directories on a website")
            
            self.console.print(help_table)
            
            # Add general help text
            self.console.print(
                "\nAutoPwnGPT accepts natural language commands. Just describe what you want to do, "
                "and AutoPwnGPT will figure out how to do it.\n",
                style="italic"
            )
        elif topic == "scanning":
            # Scanning help
            scanning_md = """
# Scanning Commands

AutoPwnGPT supports various scanning operations:

## Port Scanning
- `scan 192.168.1.1`
- `scan 192.168.1.0/24`
- `scan example.com -p 80,443`
- `scan 10.0.0.1 -p 1-1000 -sV`

## Web Scanning
- `scan https://example.com`
- `find vulnerabilities on https://example.com`
- `enumerate directories on https://example.com`
- `test sql injection on https://example.com/login.php`

## Network Scanning
- `discover hosts on 192.168.1.0/24`
- `scan network 10.0.0.0/16`
"""
            self.console.print(Markdown(scanning_md))
        elif topic == "exploitation":
            # Exploitation help
            exploitation_md = """
# Exploitation Commands

AutoPwnGPT supports various exploitation techniques:

## Web Exploitation
- `test sql injection on https://example.com/login.php`
- `exploit xss on https://example.com/search`
- `check for command injection in https://example.com/ping`

## Brute Force
- `brute force ssh on 192.168.1.1`
- `crack password for admin on https://example.com/login`
"""
            self.console.print(Markdown(exploitation_md))
        else:
            # Unknown topic
            self.console.print(f"No help available for topic: {topic}", style="yellow")
            self.console.print("Try 'help', 'help scanning', or 'help exploitation'", style="yellow")
    
    def _display_version(self) -> None:
        """Display version information."""
        version = self.config.get("application", {}).get("version", "0.1.0")
        self.console.print(f"AutoPwnGPT version {version}", style="bold blue")
    
    def _display_modules(self, category: str = "all") -> None:
        """
        Display available modules.
        
        Args:
            category: Module category to display.
        """
        if category == "all":
            # Get all modules
            modules = self.engine.get_available_modules()
        else:
            # Get modules by category
            modules = self.engine.get_modules_by_category(category)
        
        if not modules:
            self.console.print(f"No modules found in category: {category}", style="yellow")
            return
        
        # Create table for modules
        modules_table = Table(title=f"Available Modules ({category})")
        modules_table.add_column("Name", style="cyan", no_wrap=True)
        modules_table.add_column("Description", style="green")
        modules_table.add_column("Version", style="blue")
        
        # Add modules to table
        for name, info in modules.items():
            modules_table.add_row(
                name, 
                info.get("description", ""), 
                info.get("version", "")
            )
        
        self.console.print(modules_table)
    
    def _display_result(self, task_id: str, result: Any) -> None:
        """
        Display module execution result.
        
        Args:
            task_id: Task ID.
            result: Execution result.
        """
        if result.success:
            self.console.print(f"[bold green]Task {task_id} completed successfully[/bold green]")
            
            # Display findings
            if result.findings:
                self.console.print(f"\n[bold]Found {len(result.findings)} issue(s):[/bold]")
                
                for i, finding in enumerate(result.findings):
                    # Determine panel color based on severity
                    color = {
                        "critical": "red",
                        "high": "magenta",
                        "medium": "yellow",
                        "low": "blue",
                        "info": "green"
                    }.get(finding.severity.value, "white")
                    
                    # Create finding panel
                    self.console.print(
                        Panel(
                            f"{finding.description}\n\n"
                            f"[bold]Remediation:[/bold]\n{finding.remediation or 'N/A'}",
                            title=f"[{i+1}] {finding.title}",
                            border_style=color,
                            title_align="left",
                        )
                    )
            else:
                self.console.print("[green]No issues found.[/green]")
            
            # Display raw output if available
            if result.raw_output:
                # Check if user wants to see raw output
                self.console.print("\nDetailed results available. Display? [y/N]", end="")
                display_raw = input(" ").lower() == "y"
                
                if display_raw:
                    raw_json = json.dumps(result.raw_output, indent=2)
                    self.console.print(Syntax(raw_json, "json", theme="monokai", line_numbers=True))
        else:
            # Execution failed
            self.console.print(f"[bold red]Task {task_id} failed:[/bold red] {result.error_message}")
    
    def _save_session(self, filename: str) -> None:
        """
        Save the current session.
        
        Args:
            filename: Filename to save to.
        """
        # Validate filename
        if not filename:
            self.console.print("Please specify a filename", style="yellow")
            return
        
        # Make sure session directory exists
        session_dir = os.path.dirname(filename)
        if session_dir and not os.path.exists(session_dir):
            os.makedirs(session_dir, exist_ok=True)
        
        # Save context
        if self.engine.save_context(filename):
            self.console.print(f"Session saved to {filename}", style="green")
        else:
            self.console.print(f"Failed to save session to {filename}", style="red")
    
    def load_session(self, filename: str) -> None:
        """
        Load a saved session.
        
        Args:
            filename: Filename to load from.
        """
        # Validate filename
        if not filename:
            self.console.print("Please specify a filename", style="yellow")
            return
        
        # Check if file exists
        if not os.path.exists(filename):
            self.console.print(f"File not found: {filename}", style="red")
            return
        
        # Load context
        if self.engine.load_context(filename):
            self.console.print(f"Session loaded from {filename}", style="green")
        else:
            self.console.print(f"Failed to load session from {filename}", style="red")
