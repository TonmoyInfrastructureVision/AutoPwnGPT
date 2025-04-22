#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Manager for AutoPwnGPT.
Handles module discovery, loading, and execution management.
"""

import importlib
import inspect
import logging
import os
import pkgutil
import sys
from typing import Any, Dict, List, Optional, Set, Tuple, Type

from src.modules.base_module import BaseModule, ModuleResult


class ModuleManager:
    """
    Manages the discovery, loading, and execution of modules.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the module manager.
        
        Args:
            config: The configuration dictionary.
        """
        self.logger = logging.getLogger("autopwngpt.core.module_manager")
        self.config = config
        self.modules = {}  # name -> module class
        self.module_instances = {}  # name -> module instance
        self.module_directories = self.config.get("modules", {}).get("module_directories", ["src/modules"])
        
        # Ensure all module directories are in the Python path
        for directory in self.module_directories:
            if directory not in sys.path and os.path.exists(directory):
                sys.path.append(directory)
        
        # Load all available modules
        self.discover_modules()
    
    def discover_modules(self) -> None:
        """
        Discover all available modules in the module directories.
        """
        self.logger.info("Discovering modules...")
        
        # Clear current modules
        self.modules = {}
        
        # Discover modules in each directory
        for module_dir in self.module_directories:
            if not os.path.exists(module_dir):
                self.logger.warning(f"Module directory not found: {module_dir}")
                continue
            
            self._discover_modules_in_directory(module_dir)
        
        self.logger.info(f"Discovered {len(self.modules)} modules")
    
    def _discover_modules_in_directory(self, directory: str) -> None:
        """
        Discover modules in a specific directory.
        
        Args:
            directory: The directory to search for modules.
        """
        # Get the package name from the directory path
        package_name = os.path.basename(directory)
        if package_name == "modules":
            package_name = "src.modules"
        
        # Import the package
        try:
            package = importlib.import_module(package_name)
        except ImportError as e:
            self.logger.error(f"Failed to import package {package_name}: {str(e)}")
            return
        
        # Walk through all modules in the package
        for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
            # Skip __init__ and base_module
            if module_name.endswith('__init__') or module_name.endswith('base_module'):
                continue
            
            # Import the module
            try:
                module = importlib.import_module(module_name)
                
                # Find all classes in the module that inherit from BaseModule
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (issubclass(obj, BaseModule) and 
                            obj is not BaseModule and 
                            obj.__module__ == module_name):
                        module_instance = obj()
                        self.modules[module_instance.name] = obj
                        self.logger.debug(f"Discovered module: {module_instance.name}")
            
            except Exception as e:
                self.logger.error(f"Failed to load module {module_name}: {str(e)}")
    
    def get_module(self, name: str) -> Optional[Type[BaseModule]]:
        """
        Get a module class by name.
        
        Args:
            name: The name of the module.
            
        Returns:
            The module class if found, None otherwise.
        """
        return self.modules.get(name)
    
    def get_module_instance(self, name: str, context: Optional[Dict[str, Any]] = None) -> Optional[BaseModule]:
        """
        Get or create a module instance by name.
        
        Args:
            name: The name of the module.
            context: The context to initialize the module with.
            
        Returns:
            The module instance if found, None otherwise.
        """
        # Check if we already have an instance
        if name in self.module_instances:
            # Update context if provided
            if context:
                self.module_instances[name].update_context(context)
            return self.module_instances[name]
        
        # Get the module class
        module_class = self.get_module(name)
        if not module_class:
            self.logger.error(f"Module not found: {name}")
            return None
        
        # Create a new instance
        instance = module_class(context=context or {})
        self.module_instances[name] = instance
        return instance
    
    def get_all_modules(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all available modules.
        
        Returns:
            A dictionary mapping module names to module information.
        """
        return {name: module_class.get_info() for name, module_class in self.modules.items()}
    
    def get_modules_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """
        Get modules by category.
        
        Args:
            category: The category of modules to retrieve.
            
        Returns:
            A dictionary mapping module names to module information.
        """
        modules = {}
        for name, module_class in self.modules.items():
            if category.lower() in name.lower():
                modules[name] = module_class.get_info()
        return modules
    
    async def execute_module(self, name: str, args: Optional[Dict[str, Any]] = None, 
                            context: Optional[Dict[str, Any]] = None) -> ModuleResult:
        """
        Execute a module by name.
        
        Args:
            name: The name of the module to execute.
            args: Arguments for the module execution.
            context: Context for the module execution.
            
        Returns:
            The result of the module execution.
        """
        # Get the module instance
        instance = self.get_module_instance(name, context)
        if not instance:
            return ModuleResult(
                success=False,
                error_message=f"Module not found: {name}"
            )
        
        # Execute the module
        self.logger.info(f"Executing module: {name}")
        result = await instance.execute(args or {})
        return result
    
    def get_module_dependencies(self, name: str) -> List[str]:
        """
        Get the dependencies of a module.
        
        Args:
            name: The name of the module.
            
        Returns:
            A list of module names that this module depends on.
        """
        module_class = self.get_module(name)
        if not module_class:
            return []
        
        instance = module_class()
        return instance.dependencies
    
    def check_dependencies(self, name: str) -> Tuple[bool, List[str]]:
        """
        Check if all dependencies of a module are available.
        
        Args:
            name: The name of the module.
            
        Returns:
            A tuple of (dependencies_met, missing_dependencies).
        """
        dependencies = self.get_module_dependencies(name)
        if not dependencies:
            return True, []
        
        missing = []
        for dep in dependencies:
            if dep not in self.modules:
                missing.append(dep)
        
        return len(missing) == 0, missing
