# # AutoPwnGPT Task Scheduler

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision
# Date: 2025-04-22

import asyncio
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor

class TaskPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class Task:
    id: str
    function: Callable
    args: tuple
    kwargs: dict
    priority: TaskPriority
    created_at: datetime
    dependencies: List[str] = []  # Changed from None to empty list
    timeout: int = 300  # Default timeout of 5 minutes

class TaskScheduler:
    def __init__(self, max_concurrent_tasks: int = 5):
        self.tasks: Dict[str, Task] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.completed_tasks: Dict[str, Any] = {}
        self.failed_tasks: Dict[str, Exception] = {}
        self.max_concurrent_tasks = max_concurrent_tasks
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)
        self.logger = logging.getLogger(__name__)

    async def schedule_task(self, task: Task) -> str:
        """Schedule a new task for execution."""
        self.tasks[task.id] = task
        self.logger.info(f"Scheduled task {task.id} with priority {task.priority}")
        await self._process_queue()
        return task.id

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled or running task."""
        if task_id in self.running_tasks:
            self.running_tasks[task_id].cancel()
            self.logger.info(f"Cancelled running task {task_id}")
            return True
        elif task_id in self.tasks:
            del self.tasks[task_id]
            self.logger.info(f"Cancelled scheduled task {task_id}")
            return True
        return False

    async def get_task_status(self, task_id: str) -> dict:
        """Get the current status of a task."""
        if task_id in self.completed_tasks:
            return {"status": "completed", "result": self.completed_tasks[task_id]}
        elif task_id in self.failed_tasks:
            return {"status": "failed", "error": str(self.failed_tasks[task_id])}
        elif task_id in self.running_tasks:
            return {"status": "running"}
        elif task_id in self.tasks:
            return {"status": "scheduled"}
        return {"status": "not_found"}

    async def _process_queue(self):
        """Process the task queue based on priorities and dependencies."""
        if len(self.running_tasks) >= self.max_concurrent_tasks:
            return

        # Sort tasks by priority
        sorted_tasks = sorted(
            self.tasks.items(),
            key=lambda x: (x[1].priority.value, x[1].created_at),
            reverse=True
        )

        for task_id, task in sorted_tasks:
            if await self._can_run_task(task):
                await self._execute_task(task)

    async def _can_run_task(self, task: Task) -> bool:
        """Check if a task can be run based on its dependencies."""
        if not task.dependencies:
            return True

        return all(
            dep_id in self.completed_tasks
            for dep_id in task.dependencies
        )

    async def _execute_task(self, task: Task):
        """Execute a task with timeout handling."""
        if task.id in self.tasks:
            del self.tasks[task.id]

        async def wrapped_task():
            try:
                # Execute the task in a thread pool to avoid blocking
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    task.function,
                    *task.args,
                    **task.kwargs
                )
                self.completed_tasks[task.id] = result
                self.logger.info(f"Task {task.id} completed successfully")
            except Exception as e:
                self.failed_tasks[task.id] = e
                self.logger.error(f"Task {task.id} failed with error: {str(e)}")
            finally:
                if task.id in self.running_tasks:
                    del self.running_tasks[task.id]

        task_coroutine = asyncio.create_task(wrapped_task())
        self.running_tasks[task.id] = task_coroutine

        try:
            await asyncio.wait_for(task_coroutine, timeout=task.timeout)
        except asyncio.TimeoutError:
            self.failed_tasks[task.id] = TimeoutError(f"Task {task.id} timed out after {task.timeout} seconds")
            self.logger.error(f"Task {task.id} timed out")
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]

    async def clear_completed_tasks(self):
        """Clear the history of completed tasks."""
        self.completed_tasks.clear()
        self.failed_tasks.clear()

    def get_queue_status(self) -> dict:
        """Get the current status of the task queue."""
        return {
            "scheduled": len(self.tasks),
            "running": len(self.running_tasks),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks)
        }
