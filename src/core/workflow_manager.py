# # AutoPwnGPT Workflow Manager

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision
# Date: 2025-04-22

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import logging
from dataclasses import dataclass, field
from enum import Enum
import json
import yaml

from .task_scheduler import TaskScheduler, TaskPriority, Task
from ..modules.base_module import BaseModule

class WorkflowState(Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowStep:
    module_name: str
    config: dict
    dependencies: List[str] = []  # Changed from None to empty list
    retry_count: int = 3
    timeout: int = 600  # 10 minutes default timeout

@dataclass
class Workflow:
    id: str
    name: str
    description: str
    steps: List[WorkflowStep]  # Fixed syntax
    created_at: datetime
    state: WorkflowState
    results: Dict[str, Any] = field(default_factory=dict)  # Changed from None to empty dict
    metadata: Dict[str, Any] = field(default_factory=dict)  # Changed from None to empty dict

class WorkflowManager:
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.task_scheduler = TaskScheduler()
        self.logger = logging.getLogger(__name__)
        self.active_modules: Dict[str, BaseModule] = {}

    async def create_workflow(self, name: str, description: str, steps: List[WorkflowStep]) -> str:  # Fixed syntax
        """Create a new workflow with the specified steps."""
        workflow_id = str(uuid.uuid4())
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            steps=steps,
            created_at=datetime.now(),
            state=WorkflowState.CREATED,
            results={},
            metadata={}
        )
        self.workflows[workflow_id] = workflow
        self.logger.info(f"Created new workflow: {name} (ID: {workflow_id})")
        return workflow_id

    async def start_workflow(self, workflow_id: str) -> bool:
        """Start executing a workflow."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow = self.workflows[workflow_id]
        if workflow.state != WorkflowState.CREATED:
            raise ValueError(f"Workflow {workflow_id} is already {workflow.state}")

        workflow.state = WorkflowState.RUNNING
        await self._schedule_workflow_steps(workflow)
        return True

    async def _schedule_workflow_steps(self, workflow: Workflow):
        """Schedule all steps in the workflow respecting dependencies."""
        for step in workflow.steps:
            task_id = f"{workflow.id}_{step.module_name}"
            task = Task(
                id=task_id,
                function=self._execute_module,
                args=(workflow.id, step),
                kwargs={},
                priority=TaskPriority.MEDIUM,
                created_at=datetime.now(),
                dependencies=step.dependencies,
                timeout=step.timeout
            )
            await self.task_scheduler.schedule_task(task)

    async def _execute_module(self, workflow_id: str, step: WorkflowStep) -> Dict[str, Any]:
        """Execute a single module within a workflow."""
        try:
            # Import the module dynamically
            module_class = self._import_module(step.module_name)
            module_instance = module_class(step.config)
            self.active_modules[f"{workflow_id}_{step.module_name}"] = module_instance

            # Execute the module
            result = await module_instance.run()
            
            # Store the results
            workflow = self.workflows[workflow_id]
            workflow.results[step.module_name] = result

            return result
        except Exception as e:
            self.logger.error(f"Error executing module {step.module_name}: {str(e)}")
            raise

    def _import_module(self, module_name: str) -> type:
        """Dynamically import a module class."""
        try:
            # Assuming modules are in the modules package
            module_path = f"..modules.{module_name}"
            import importlib
            module = importlib.import_module(module_path, package=__package__)
            return getattr(module, module_name.title())
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not import module {module_name}: {str(e)}")

    async def pause_workflow(self, workflow_id: str) -> bool:
        """Pause a running workflow."""
        if workflow_id not in self.workflows:
            return False

        workflow = self.workflows[workflow_id]
        if workflow.state != WorkflowState.RUNNING:
            return False

        workflow.state = WorkflowState.PAUSED
        # Cancel all pending tasks for this workflow
        tasks = await self._get_workflow_tasks(workflow_id)
        for task_id in tasks:
            await self.task_scheduler.cancel_task(task_id)
        return True

    async def resume_workflow(self, workflow_id: str) -> bool:
        """Resume a paused workflow."""
        if workflow_id not in self.workflows:
            return False

        workflow = self.workflows[workflow_id]
        if workflow.state != WorkflowState.PAUSED:
            return False

        workflow.state = WorkflowState.RUNNING
        await self._schedule_workflow_steps(workflow)
        return True

    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a workflow and clean up resources."""
        if workflow_id not in self.workflows:
            return False

        workflow = self.workflows[workflow_id]
        workflow.state = WorkflowState.CANCELLED
        
        # Cancel all tasks and cleanup modules
        tasks = await self._get_workflow_tasks(workflow_id)
        for task_id in tasks:
            await self.task_scheduler.cancel_task(task_id)
        
        # Cleanup active modules
        for module_id in list(self.active_modules.keys()):
            if module_id.startswith(workflow_id):
                await self.active_modules[module_id].cleanup()
                del self.active_modules[module_id]

        return True

    async def _get_workflow_tasks(self, workflow_id: str) -> List[str]:
        """Get all task IDs associated with a workflow."""
        return [
            task_id for task_id in self.task_scheduler.tasks.keys()
            if task_id.startswith(workflow_id)
        ]

    async def get_workflow_status(self, workflow_id: str) -> dict:
        """Get the current status of a workflow including all steps."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow = self.workflows[workflow_id]
        tasks = await self._get_workflow_tasks(workflow_id)
        
        step_statuses = {}
        for step in workflow.steps:
            task_id = f"{workflow_id}_{step.module_name}"
            status = await self.task_scheduler.get_task_status(task_id)
            step_statuses[step.module_name] = status

        return {
            "id": workflow.id,
            "name": workflow.name,
            "state": workflow.state.value,
            "steps": step_statuses,
            "results": workflow.results,
            "created_at": workflow.created_at.isoformat(),
            "pending_tasks": len(tasks)
        }

    def save_workflow_template(self, workflow: Workflow, filepath: str):
        """Save a workflow as a template for future use."""
        template = {
            "name": workflow.name,
            "description": workflow.description,
            "steps": [
                {
                    "module_name": step.module_name,
                    "config": step.config,
                    "dependencies": step.dependencies,
                    "retry_count": step.retry_count,
                    "timeout": step.timeout
                }
                for step in workflow.steps
            ],
            "metadata": workflow.metadata
        }
        
        with open(filepath, 'w') as f:
            yaml.dump(template, f, default_flow_style=False)

    @classmethod
    def load_workflow_template(cls, filepath: str) -> Dict:
        """Load a workflow template from a file."""
        with open(filepath, 'r') as f:
            template = yaml.safe_load(f)
        return template
