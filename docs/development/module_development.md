# AutoPwnGPT Module Development

Author: Eshan Roy
Email: m.eshanized@gmail.com
GitHub: https://github.com/TonmoyInfrastructureVision
Date: 2025-04-22

# Module Development Guide

This guide explains how to develop modules for AutoPwnGPT. Modules are the building blocks that provide the actual security testing functionality.

## Module Overview

AutoPwnGPT's modular architecture allows developers to create specialized components that perform specific security testing tasks. Each module follows a standard interface, making it easy to integrate into the framework.

## Module Types

AutoPwnGPT supports several types of modules:

- **Scanner Modules**: Discover hosts, services, and information
- **Enumeration Modules**: Gather detailed information about targets
- **Exploit Modules**: Execute attacks against vulnerabilities
- **Post-Exploitation Modules**: Perform actions after successful compromise
- **Brute Force Modules**: Test authentication mechanisms
- **Web Modules**: Test web applications
- **Payload Modules**: Generate payloads for various attacks

## Creating a New Module

### 1. Module Template

Start by copying the module template from `data/templates/module_template.py`:

```bash
cp data/templates/module_template.py src/modules/custom/my_module.py
```

### 2. Basic Structure

Every module must implement the `BaseModule` interface:

```python
from typing import Dict, Any, List, Optional
from src.modules.base_module import BaseModule

class MyCustomModule(BaseModule):
    """
    My custom module that does X.
    
    This module provides functionality for...
    """
    
    def __init__(self):
        """Initialize the module with default configuration."""
        super().__init__(
            name="my_custom_module",
            description="A module that performs X functionality",
            author="Your Name",
            version="0.1.0"
        )
        
        # Define module parameters
        self.register_parameter(
            name="target",
            description="Target to scan",
            required=True,
            parameter_type=str
        )
        
        self.register_parameter(
            name="timeout",
            description="Operation timeout in seconds",
            required=False,
            parameter_type=int,
            default=30
        )
    
    def validate_parameters(self) -> bool:
        """Validate that the provided parameters are correct."""
        # Perform custom validation
        return True
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the module's main functionality.
        
        Returns:
            Dict containing the results of the module execution
        """
        # Get parameters
        target = self.get_parameter("target")
        timeout = self.get_parameter("timeout")
        
        # Implement module logic here
        results = self._perform_operation(target, timeout)
        
        # Return results in a standardized format
        return {
            "status": "success",
            "findings": results,
            "metadata": {
                "timestamp": self._get_timestamp(),
                "module_version": self.version
            }
        }
    
    def _perform_operation(self, target: str, timeout: int) -> List[Dict[str, Any]]:
        """Internal method to perform the actual operation."""
        # Implement your core functionality here
        pass

### 3. Module Registration

To make your module available in the system, register it in the appropriate module category file:

```python
# In src/modules/custom/__init__.py
from src.modules.custom.my_module import MyCustomModule

__all__ = ["MyCustomModule"]
```

And update the main module registry:

```python
# In src/modules/__init__.py
from src.modules.custom import MyCustomModule

# Add to the modules dictionary
AVAILABLE_MODULES = {
    # ... existing modules ...
    "my_custom_module": MyCustomModule
}
```

## Module Best Practices

### Error Handling

Always handle errors gracefully:

```python
def run(self) -> Dict[str, Any]:
    try:
        # Module operation
        return {"status": "success", "data": result}
    except Exception as e:
        self.logger.error(f"Module execution failed: {str(e)}")
        return {"status": "error", "message": str(e)}
```

### Logging

Use the built-in logging system:

```python
def _perform_operation(self, target: str) -> List[Dict[str, Any]]:
    self.logger.info(f"Starting operation on {target}")
    # ... operation code ...
    self.logger.debug(f"Found {len(results)} results")
    return results
```

### Progress Reporting

For long-running operations, report progress:

```python
def run(self) -> Dict[str, Any]:
    total_steps = 5
    
    self.report_progress(0, total_steps, "Initializing")
    # Step 1
    
    self.report_progress(1, total_steps, "Connecting to target")
    # Step 2
    
    # ... more steps ...
    
    self.report_progress(total_steps, total_steps, "Completed")
    return results
```

### Documentation

Document your module thoroughly:

1. Class docstring explaining purpose and functionality
2. Method docstrings with parameters and return values
3. Example usage
4. Dependencies and requirements

## Testing Modules

Create unit tests for your module in the `tests/unit/modules/` directory:

```python
# tests/unit/modules/test_my_module.py
import pytest
from src.modules.custom.my_module import MyCustomModule

def test_module_initialization():
    module = MyCustomModule()
    assert module.name == "my_custom_module"
    assert module.version == "0.1.0"

def test_parameter_validation():
    module = MyCustomModule()
    module.set_parameter("target", "192.168.1.1")
    assert module.validate_parameters() is True
    
    module.set_parameter("target", "")
    assert module.validate_parameters() is False

# Add more tests for the module's functionality
```

## Example Modules

For reference, check these example modules:

- [Network Scanner](../examples/basic/network_scanner.py)
- [Web Scanner](../examples/basic/web_scanner.py)
- [Custom Module Example](../examples/custom_modules/custom_module_example.py)

---

Author: Eshan Roy  
Email: m.eshanized@gmail.com  
GitHub: https://github.com/TonmoyInfrastructureVision
