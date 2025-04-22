#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AutoPwnGPT Engine Module.
Core coordinator for the execution of modules and workflows.
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from src.core.module_manager import ModuleManager
from src.core.context_manager import ContextManager
from src.modules.base_module import ModuleResult


class Engine:
    """
    Core engine for AutoPwnGPT.
    Coordinates the execution of modules and workflows.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the engine.
        
        Args:
            config: Configuration dictionary.
        """
        self.logger = logging.getLogger("autopwngpt.core.engine")
        self.config = config
        self.module_manager = ModuleManager(config)
        self.context_manager = ContextManager()
        self.running_tasks = {}  # task_id -> asyncio.Task
        self.task_results = {}  # task_id -> ModuleResult
        self.next_task_id = 1
    
    async def execute_module(self, module_name: str, args: Dict[str, Any] = None) -> Tuple[str, ModuleResult]:
        """
        Execute a module with the given arguments.
        
        Args:
            module_name: The name of the module to execute.
            args: Arguments for the module execution.
            
        Returns:
            A tuple of (task_id, result).
        """
        # Get context for the module
        context = self.context_manager.get_context()
        
        # Generate a task ID
        task_id = f"task-{self.next_task_id}"
        self.next_task_id += 1
        
        # Execute the module
        self.logger.info(f"Executing module {module_name} with task ID {task_id}")
        result = await self.module_manager.execute_module(module_name, args, context)
        
        # Update context with results
        if result.success:
            self.context_manager.update_context({
                f"results.{module_name}": {
                    "timestamp": time.time(),
                    "findings": [f.__dict__ for f in result.findings],
                    "raw_output": result.raw_output
                }
            })
        
        # Store result
        self.task_results[task_id] = result
        
        return task_id, result
    
    async def execute_module_async(self, module_name: str, args: Dict[str, Any] = None) -> str:
        """
        Execute a module asynchronously.
        
        Args:
            module_name: The name of the module to execute.
            args: Arguments for the module execution.
            
        Returns:
            The task ID for the execution.
        """
        # Generate a task ID
        task_id = f"task-{self.next_task_id}"
        self.next_task_id += 1
        
        # Create a task for the module execution
        task = asyncio.create_task(self._execute_module_task(task_id, module_name, args))
        self.running_tasks[task_id] = task
        
        self.logger.info(f"Started async execution of module {module_name} with task ID {task_id}")
        return task_id
    
    async def _execute_module_task(self, task_id: str, module_name: str, args: Dict[str, Any] = None) -> None:
        """
        Internal method to execute a module as a task.
        
        Args:
            task_id: The ID of the task.
            module_name: The name of the module to execute.
            args: Arguments for the module execution.
        """
        try:
            # Get context for the module
            context = self.context_manager.get_context()
            
            # Execute the module
            result = await self.module_manager.execute_module(module_name, args, context)
            
            # Update context with results
            if result.success:
                self.context_manager.update_context({
                    f"results.{module_name}": {
                        "timestamp": time.time(),
                        "findings": [f.__dict__ for f in result.findings],
                        "raw_output": result.raw_output
                    }
                })
            
            # Store result
            self.task_results[task_id] = result
            
        except Exception as e:
            self.logger.exception(f"Error executing module {module_name}: {str(e)}")
            self.task_results[task_id] = ModuleResult(
                success=False,
                error_message=f"Execution error: {str(e)}"
            )
        finally:
            # Remove task from running tasks
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a running task.
        
        Args:
            task_id: The ID of the task to cancel.
            
        Returns:
            True if the task was cancelled, False otherwise.
        """
        if task_id in self.running_tasks:
            task = self.running_tasks[task_id]
            task.cancel()
            self.logger.info(f"Cancelled task {task_id}")
            return True
        return False
    
    def get_task_result(self, task_id: str) -> Optional[ModuleResult]:
        """
        Get the result of a task.
        
        Args:
            task_id: The ID of the task.
            
        Returns:
            The result of the task, or None if not found.
        """
        return self.task_results.get(task_id)
    
    def is_task_running(self, task_id: str) -> bool:
        """
        Check if a task is still running.
        
        Args:
            task_id: The ID of the task.
            
        Returns:
            True if the task is running, False otherwise.
        """
        return task_id in self.running_tasks
    
    def get_available_modules(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all available modules.
        
        Returns:
            A dictionary mapping module names to module information.
        """
        return self.module_manager.get_all_modules()
    
    def get_modules_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """
        Get modules by category.
        
        Args:
            category: The category of modules to retrieve.
            
        Returns:
            A dictionary mapping module names to module information.
        """
        return self.module_manager.get_modules_by_category(category)
    
    async def execute_workflow(self, workflow: List[Dict[str, Any]]) -> Dict[str, ModuleResult]:
        """
        Execute a series of modules in sequence.
        
        Args:
            workflow: A list of workflow steps, each with 'module' and 'args' keys.
            
        Returns:
            A dictionary mapping step names to results.
        """
        results = {}
        
        for i, step in enumerate(workflow):
            if 'module' not in step:
                self.logger.error(f"Missing 'module' key in workflow step {i}")
                continue
                
            module_name = step['module']
            args = step.get('args', {})
            step_name = step.get('name', f"step-{i+1}")
            
            self.logger.info(f"Executing workflow step {step_name}: {module_name}")
            _, result = await self.execute_module(module_name, args)
            results[step_name] = result
            
            # If the step failed and it's not configured to continue on failure, stop the workflow
            if not result.success and not step.get('continue_on_failure', False):
                self.logger.warning(f"Workflow step {step_name} failed, stopping workflow")
                break
        
        return results
    
    def reset_context(self) -> None:
        """
        Reset the context to its initial state.
        """
        self.context_manager.reset_context()
        self.logger.info("Context reset to initial state")
    
    def get_context(self) -> Dict[str, Any]:
        """
        Get the current context.
        
        Returns:
            The current context dictionary.
        """
        return self.context_manager.get_context()
    
    def update_context(self, updates: Dict[str, Any]) -> None:
        """
        Update the context with new data.
        
        Args:
            updates: Dictionary of updates to apply to the context.
        """
        self.context_manager.update_context(updates)
    
    def save_context(self, filename: str) -> bool:
        """
        Save the current context to a file.
        
        Args:
            filename: The filename to save to.
            
        Returns:
            True if successful, False otherwise.
        """
        return self.context_manager.save_context(filename)
    
    def load_context(self, filename: str) -> bool:
        """
        Load context from a file.
        
        Args:
            filename: The filename to load from.
            
        Returns:
            True if successful, False otherwise.
        """
        return self.context_manager.load_context(filename)
