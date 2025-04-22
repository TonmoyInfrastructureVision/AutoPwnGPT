#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base module definition for AutoPwnGPT.
This module provides the abstract base class that all modules must inherit from.
"""

from abc import ABC, abstractmethod
import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class ModuleStatus(Enum):
    """Status of a module's execution."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ModuleSeverity(Enum):
    """Severity level of a finding."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ModuleFinding:
    """A finding from a module's execution."""
    title: str
    description: str
    severity: ModuleSeverity
    timestamp: float = field(default_factory=time.time)
    details: Dict[str, Any] = field(default_factory=dict)
    evidence: Optional[str] = None
    remediation: Optional[str] = None
    references: List[str] = field(default_factory=list)


@dataclass
class ModuleResult:
    """Result of a module's execution."""
    success: bool
    findings: List[ModuleFinding] = field(default_factory=list)
    raw_output: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    error_message: Optional[str] = None


class BaseModule(ABC):
    """
    Abstract base class for all AutoPwnGPT modules.
    
    All modules must inherit from this class and implement the required methods.
    """
    
    def __init__(self, context: Dict[str, Any] = None):
        """
        Initialize the module.
        
        Args:
            context: The context data for the module execution.
        """
        self.name = self.__class__.__name__
        self.description = self.__doc__ or "No description provided"
        self.version = "1.0.0"
        self.status = ModuleStatus.IDLE
        self.context = context or {}
        self.dependencies = []
        self.required_args = []
        self.optional_args = {}
        self.logger = logging.getLogger(f"autopwngpt.modules.{self.name}")
        self.start_time = None
        self.end_time = None
    
    def __str__(self) -> str:
        """String representation of the module."""
        return f"{self.name} (v{self.version})"
    
    def set_context(self, context: Dict[str, Any]) -> None:
        """
        Set the execution context for the module.
        
        Args:
            context: The context data.
        """
        self.context = context
    
    def update_context(self, new_context_data: Dict[str, Any]) -> None:
        """
        Update the execution context with new data.
        
        Args:
            new_context_data: New data to add to the context.
        """
        self.context.update(new_context_data)
    
    def validate_args(self, args: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate the arguments for the module.
        
        Args:
            args: The arguments to validate.
            
        Returns:
            A tuple of (is_valid, error_message).
        """
        # Check for required arguments
        for arg in self.required_args:
            if arg not in args:
                return False, f"Missing required argument: {arg}"
        
        return True, None
    
    async def execute(self, args: Dict[str, Any] = None) -> ModuleResult:
        """
        Execute the module with the provided arguments.
        
        Args:
            args: Arguments for the module execution.
            
        Returns:
            The result of the module execution.
        """
        args = args or {}
        self.start_time = time.time()
        self.status = ModuleStatus.RUNNING
        
        # Validate arguments
        is_valid, error_message = self.validate_args(args)
        if not is_valid:
            self.status = ModuleStatus.FAILED
            self.end_time = time.time()
            return ModuleResult(
                success=False,
                error_message=error_message,
                execution_time=self.end_time - self.start_time
            )
        
        try:
            # Execute the module implementation
            self.logger.info(f"Executing module {self.name}")
            result = await self._execute(args)
            self.status = ModuleStatus.COMPLETED
        except Exception as e:
            self.logger.exception(f"Error executing module {self.name}: {str(e)}")
            self.status = ModuleStatus.FAILED
            self.end_time = time.time()
            return ModuleResult(
                success=False,
                error_message=str(e),
                execution_time=self.end_time - self.start_time
            )
        
        self.end_time = time.time()
        execution_time = self.end_time - self.start_time
        
        # Add execution time to the result
        result.execution_time = execution_time
        
        self.logger.info(f"Module {self.name} completed in {execution_time:.2f}s")
        return result
    
    def cancel(self) -> None:
        """Cancel the module execution."""
        if self.status == ModuleStatus.RUNNING:
            self.status = ModuleStatus.CANCELLED
            self.logger.info(f"Module {self.name} cancelled")
    
    @abstractmethod
    async def _execute(self, args: Dict[str, Any]) -> ModuleResult:
        """
        Actual implementation of the module execution.
        
        Args:
            args: Arguments for the module execution.
            
        Returns:
            The result of the module execution.
        """
        pass
    
    @classmethod
    def get_info(cls) -> Dict[str, Any]:
        """
        Get information about the module.
        
        Returns:
            A dictionary containing module information.
        """
        instance = cls()
        return {
            "name": instance.name,
            "description": instance.description,
            "version": instance.version,
            "required_args": instance.required_args,
            "optional_args": instance.optional_args,
            "dependencies": instance.dependencies
        }
