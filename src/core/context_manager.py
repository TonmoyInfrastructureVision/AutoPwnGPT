#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Context Manager for AutoPwnGPT.
Maintains and manages stateful session context for operations.
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class ContextManager:
    """
    Manages the contextual state of a session.
    Provides methods to get, update, and manipulate context data.
    """
    
    def __init__(self):
        """Initialize the context manager with an empty context."""
        self.logger = logging.getLogger("autopwngpt.core.context_manager")
        self.reset_context()
    
    def reset_context(self) -> None:
        """Reset the context to its initial state."""
        self.context = {
            "session": {
                "id": self._generate_session_id(),
                "start_time": time.time(),
                "last_updated": time.time()
            },
            "targets": {},
            "findings": {},
            "vars": {},
            "results": {},
            "meta": {}
        }
        self.logger.debug("Context reset to initial state")
    
    def _generate_session_id(self) -> str:
        """
        Generate a unique session ID.
        
        Returns:
            A unique session ID.
        """
        return f"session-{int(time.time())}"
    
    def get_context(self) -> Dict[str, Any]:
        """
        Get the current context.
        
        Returns:
            The current context dictionary.
        """
        return self.context
    
    def update_context(self, updates: Dict[str, Any]) -> None:
        """
        Update the context with new data.
        
        Args:
            updates: Dictionary of updates to apply to the context.
        """
        self._apply_updates(self.context, updates)
        self.context["session"]["last_updated"] = time.time()
        self.logger.debug("Context updated")
    
    def _apply_updates(self, target: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """
        Recursively apply updates to a target dictionary.
        
        Args:
            target: The target dictionary to update.
            updates: The updates to apply.
        """
        for key, value in updates.items():
            # Handle dotted paths (e.g., "results.scan.hosts")
            if "." in key:
                parts = key.split(".", 1)
                current_key, rest_path = parts
                
                # Create nested dictionaries if they don't exist
                if current_key not in target:
                    target[current_key] = {}
                
                # Recursively apply updates to nested dictionary
                self._apply_updates(target[current_key], {rest_path: value})
            else:
                # Update or create the key
                if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                    # Merge dictionaries
                    self._apply_updates(target[key], value)
                else:
                    # Replace or create value
                    target[key] = value
    
    def get_value(self, path: str, default: Any = None) -> Any:
        """
        Get a value from the context using a dotted path.
        
        Args:
            path: The dotted path to the value (e.g., "results.scan.hosts").
            default: The default value to return if the path doesn't exist.
            
        Returns:
            The value at the path, or the default if not found.
        """
        parts = path.split(".")
        current = self.context
        
        try:
            for part in parts:
                current = current[part]
            return current
        except (KeyError, TypeError):
            return default
    
    def set_value(self, path: str, value: Any) -> None:
        """
        Set a value in the context using a dotted path.
        
        Args:
            path: The dotted path to set (e.g., "results.scan.hosts").
            value: The value to set.
        """
        self.update_context({path: value})
    
    def add_target(self, target_id: str, target_data: Dict[str, Any]) -> None:
        """
        Add a target to the context.
        
        Args:
            target_id: The ID of the target.
            target_data: Data about the target.
        """
        self.update_context({f"targets.{target_id}": target_data})
    
    def add_finding(self, finding_id: str, finding_data: Dict[str, Any]) -> None:
        """
        Add a finding to the context.
        
        Args:
            finding_id: The ID of the finding.
            finding_data: Data about the finding.
        """
        finding_data["timestamp"] = finding_data.get("timestamp", time.time())
        self.update_context({f"findings.{finding_id}": finding_data})
    
    def get_targets(self) -> Dict[str, Any]:
        """
        Get all targets in the context.
        
        Returns:
            Dictionary of targets.
        """
        return self.context.get("targets", {})
    
    def get_findings(self) -> Dict[str, Any]:
        """
        Get all findings in the context.
        
        Returns:
            Dictionary of findings.
        """
        return self.context.get("findings", {})
    
    def get_results(self) -> Dict[str, Any]:
        """
        Get all results in the context.
        
        Returns:
            Dictionary of results.
        """
        return self.context.get("results", {})
    
    def set_variable(self, name: str, value: Any) -> None:
        """
        Set a variable in the context.
        
        Args:
            name: The name of the variable.
            value: The value of the variable.
        """
        self.update_context({f"vars.{name}": value})
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """
        Get a variable from the context.
        
        Args:
            name: The name of the variable.
            default: The default value to return if the variable doesn't exist.
            
        Returns:
            The value of the variable, or the default if not found.
        """
        return self.get_value(f"vars.{name}", default)
    
    def save_context(self, filename: str) -> bool:
        """
        Save the current context to a file.
        
        Args:
            filename: The filename to save to.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(self.context, f, indent=2)
            self.logger.info(f"Context saved to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving context to {filename}: {str(e)}")
            return False
    
    def load_context(self, filename: str) -> bool:
        """
        Load context from a file.
        
        Args:
            filename: The filename to load from.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            with open(filename, 'r') as f:
                loaded_context = json.load(f)
            
            # Update session information
            current_session = self.context.get("session", {})
            loaded_context["session"] = loaded_context.get("session", {})
            loaded_context["session"]["id"] = current_session.get("id", self._generate_session_id())
            loaded_context["session"]["load_time"] = time.time()
            loaded_context["session"]["last_updated"] = time.time()
            
            # Replace context with loaded context
            self.context = loaded_context
            self.logger.info(f"Context loaded from {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error loading context from {filename}: {str(e)}")
            return False
