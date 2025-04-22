#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for AutoPwnGPT.
Initializes the application and starts the CLI or GUI.
"""

import argparse
import asyncio
import logging
import os
import sys
import yaml
import json
from typing import Dict, Any

from src.core.engine import Engine
from src.core.command_processor import CommandProcessor
from src.llm_integration.llm_manager import LlmManager
from src.cli import CliInterface


def setup_logging(config: Dict[str, Any]) -> None:
    """
    Set up logging configuration.
    
    Args:
        config: Configuration dictionary.
    """
    # Get log level from config
    log_level_str = config.get("application", {}).get("log_level", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Get log directory from config
    log_dir = config.get("application", {}).get("log_directory", "data/logs")
    
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "autopwngpt.log")),
            logging.StreamHandler()
        ]
    )
    
    # Log configuration
    logging.info(f"Logging initialized with level {log_level_str}")


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load the configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file.
        
    Returns:
        Configuration dictionary.
    """
    # Check if config file exists
    if not os.path.exists(config_path):
        print(f"Configuration file not found: {config_path}")
        return {}
    
    # Load configuration
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Override with environment variables
        if "llm" in config and "api_key" in config["llm"]:
            config["llm"]["api_key"] = os.environ.get("OPENAI_API_KEY", config["llm"]["api_key"])
        
        return config
    
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return {}


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="AutoPwnGPT - Natural Language Penetration Testing Tool")
    
    parser.add_argument(
        "--config", 
        type=str, 
        default="config.yaml", 
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--gui", 
        action="store_true", 
        help="Start with GUI instead of CLI"
    )
    
    parser.add_argument(
        "--command", 
        type=str, 
        help="Execute a single command and exit"
    )
    
    parser.add_argument(
        "--load-session", 
        type=str, 
        help="Load session from file"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging"
    )
    
    parser.add_argument(
        "--offline", 
        action="store_true", 
        help="Run in offline mode (use local LLM)"
    )
    
    return parser.parse_args()


async def main():
    """Main entry point for the application."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.debug:
        config.setdefault("application", {})["log_level"] = "DEBUG"
    
    if args.offline:
        config.setdefault("llm", {})["provider"] = "local"
    
    # Set up logging
    setup_logging(config)
    
    # Create logger for main
    logger = logging.getLogger("autopwngpt.main")
    logger.info("Starting AutoPwnGPT")
    
    try:
        # Initialize LLM manager
        llm_manager = LlmManager(config)
        
        # Initialize command processor
        command_processor = CommandProcessor(config, llm_manager)
        
        # Initialize engine
        engine = Engine(config)
        
        # Check if we should execute a single command
        if args.command:
            # Execute command
            logger.info(f"Executing command: {args.command}")
            command_result = await command_processor.process_command(args.command)
            
            if command_result.get("success", False):
                module = command_result.get("module")
                module_args = command_result.get("args", {})
                
                if module:
                    task_id, result = await engine.execute_module(module, module_args)
                    
                    # Print result as JSON
                    print(json.dumps({
                        "task_id": task_id,
                        "success": result.success,
                        "findings": [f.__dict__ for f in result.findings],
                        "error": result.error_message
                    }, indent=2))
                else:
                    print(json.dumps(command_result, indent=2))
            else:
                print(json.dumps(command_result, indent=2))
            
            return
        
        # Check if we should start the GUI
        if args.gui:
            # This is a placeholder - the GUI implementation would go here
            logger.info("Starting GUI")
            print("GUI mode is not yet implemented")
            return
        
        # Start CLI
        logger.info("Starting CLI")
        cli = CliInterface(config, engine, command_processor)
        
        # Load session if specified
        if args.load_session:
            cli.load_session(args.load_session)
        
        # Run CLI
        await cli.run()
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.exception(f"Error in main: {str(e)}")
    finally:
        logger.info("Exiting AutoPwnGPT")


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
