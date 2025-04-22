#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AutoPwnGPT Error Handler
Provides centralized error handling and custom exceptions for the application.

Author: Eshan Roy
Email: m.eshanized@gmail.com
GitHub: https://github.com/TonmoyInfrastructureVision
Date: 2025-04-22
"""

import logging
import sys
import traceback
from typing import Any, Dict, Optional, Type, Union
from functools import wraps

# Configure logger
logger = logging.getLogger("autopwngpt.core.error_handler")

class AutoPwnGPTError(Exception):
    """Base exception class for AutoPwnGPT"""
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ModuleError(AutoPwnGPTError):
    """Exception raised for errors in module operations"""
    pass

class ConfigurationError(AutoPwnGPTError):
    """Exception raised for configuration-related errors"""
    pass

class APIError(AutoPwnGPTError):
    """Exception raised for API-related errors"""
    pass

class WorkflowError(AutoPwnGPTError):
    """Exception raised for workflow execution errors"""
    pass

class ErrorHandler:
    """Centralized error handling for AutoPwnGPT"""
    
    def __init__(self):
        self.logger = logger
        
    def handle_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle an error and return a standardized error response
        
        Args:
            error: The exception to handle
            context: Additional context about where the error occurred
            
        Returns:
            Dict containing error details and context
        """
        error_type = type(error).__name__
        error_message = str(error)
        stack_trace = traceback.format_exc()
        
        # Log the error with context
        self.logger.error(f"{error_type}: {error_message}")
        if context:
            self.logger.error(f"Error context: {context}")
        self.logger.debug(f"Stack trace:\n{stack_trace}")
        
        # Prepare error response
        error_response = {
            "success": False,
            "error": {
                "type": error_type,
                "message": error_message,
                "code": getattr(error, "error_code", None),
                "context": context
            }
        }
        
        # Add stack trace in debug mode
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            error_response["error"]["stack_trace"] = stack_trace
            
        return error_response
    
    @staticmethod
    def catch_errors(func):
        """
        Decorator to catch and handle errors in functions
        
        Args:
            func: The function to wrap with error handling
            
        Returns:
            Wrapped function that catches and handles errors
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = ErrorHandler()
                context = {
                    "function": func.__name__,
                    "args": str(args),
                    "kwargs": str(kwargs)
                }
                return handler.handle_error(e, context)
        return wrapper
    
    def format_exception(self, exc: Exception) -> str:
        """
        Format an exception into a readable string
        
        Args:
            exc: The exception to format
            
        Returns:
            Formatted error message
        """
        if isinstance(exc, AutoPwnGPTError):
            return f"{type(exc).__name__}: {exc.message}"
        return f"{type(exc).__name__}: {str(exc)}"
    
    def log_critical_error(self, error: Exception, exit_program: bool = False):
        """
        Log a critical error and optionally exit the program
        
        Args:
            error: The critical error that occurred
            exit_program: Whether to exit the program after logging
        """
        self.logger.critical(self.format_exception(error))
        self.logger.debug(f"Stack trace:\n{traceback.format_exc()}")
        
        if exit_program:
            sys.exit(1)
    
    def create_error_response(self, 
                            message: str, 
                            error_type: Type[Exception] = AutoPwnGPTError,
                            error_code: Optional[str] = None,
                            context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a standardized error response
        
        Args:
            message: The error message
            error_type: The type of error to create
            error_code: Optional error code
            context: Additional error context
            
        Returns:
            Standardized error response dictionary
        """
        error = error_type(message, error_code)
        return self.handle_error(error, context)
