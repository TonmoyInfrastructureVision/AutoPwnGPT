#!/usr/bin/env python3
# AutoPwnGPT Logging System

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision
# Date: 2025-04-22

import logging
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class LoggingSystem:
    """
    Advanced logging system for AutoPwnGPT with support for multiple output formats,
    log rotation, and different logging levels.
    """
    
    def __init__(self, 
                 app_name: str = "AutoPwnGPT",
                 log_level: int = logging.INFO,
                 log_dir: str = "data/logs",
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5,
                 enable_console: bool = True,
                 enable_json: bool = True):
        """
        Initialize the logging system.
        
        Args:
            app_name: Name of the application
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir: Directory to store log files
            max_file_size: Maximum size of each log file before rotation
            backup_count: Number of backup files to keep
            enable_console: Enable console output
            enable_json: Enable JSON formatted logging
        """
        self.app_name = app_name
        self.log_level = log_level
        self.log_dir = Path(log_dir)
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        
        # Create logger
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(log_level)
        
        # Create log directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up handlers
        self.setup_file_handler()
        if enable_json:
            self.setup_json_handler()
        if enable_console:
            self.setup_console_handler()
            
        # Prevent logging from propagating to the root logger
        self.logger.propagate = False
    
    def setup_file_handler(self) -> None:
        """Set up rotating file handler for regular logs."""
        log_file = self.log_dir / f"{self.app_name}.log"
        file_handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def setup_json_handler(self) -> None:
        """Set up JSON format logging handler."""
        json_log_file = self.log_dir / f"{self.app_name}_json.log"
        json_handler = TimedRotatingFileHandler(
            filename=str(json_log_file),
            when='midnight',
            interval=1,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'level': record.levelname,
                    'module': record.module,
                    'message': record.getMessage(),
                    'source': f"{record.filename}:{record.lineno}"
                }
                # Check record.__dict__ for extra data
                if 'extra_data' in record.__dict__:
                    log_data.update(record.__dict__['extra_data'])
                return json.dumps(log_data)
        
        json_handler.setFormatter(JsonFormatter())
        self.logger.addHandler(json_handler)
    
    def setup_console_handler(self) -> None:
        """Set up console handler with colored output."""
        console_handler = logging.StreamHandler(sys.stdout)
        
        class ColoredFormatter(logging.Formatter):
            COLORS = {
                'DEBUG': '\033[94m',    # Blue
                'INFO': '\033[92m',     # Green
                'WARNING': '\033[93m',  # Yellow
                'ERROR': '\033[91m',    # Red
                'CRITICAL': '\033[95m', # Purple
                'RESET': '\033[0m'      # Reset
            }
            
            def format(self, record):
                color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
                # Format the message with colored level name
                return f"{color}{record.levelname}{self.COLORS['RESET']} - {record.getMessage()}"
        
        console_handler.setFormatter(ColoredFormatter())
        self.logger.addHandler(console_handler)
    
    def log(self, level: int, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a message with the specified level and optional extra data.
        
        Args:
            level: Logging level
            message: Message to log
            extra: Optional dictionary of extra data to include in JSON logs
        """
        if extra:
            self.logger.log(level, message, extra={'extra_data': extra})
        else:
            self.logger.log(level, message)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a debug message."""
        self.log(logging.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log an info message."""
        self.log(logging.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a warning message."""
        self.log(logging.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log an error message."""
        self.log(logging.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a critical message."""
        self.log(logging.CRITICAL, message, extra)
    
    def log_exception(self, message: str, exc_info: bool = True, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an exception with traceback.
        
        Args:
            message: Error message
            exc_info: Whether to include exception info
            extra: Optional extra data to include
        """
        self.logger.exception(message, exc_info=exc_info, extra={'extra_data': extra} if extra else None)
    
    def set_level(self, level: int) -> None:
        """
        Set the logging level.
        
        Args:
            level: New logging level
        """
        self.logger.setLevel(level)
        self.log_level = level
    
    def clear_handlers(self) -> None:
        """Remove all handlers from the logger."""
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()
