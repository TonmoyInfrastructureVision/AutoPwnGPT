# AutoPwnGPT Module Development

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision
# Date: 2025-04-23

---

This guide explains how to create, structure, and integrate new modules into the AutoPwnGPT framework. Modules are the core building blocks for extending the tool's capabilities.

## Table of Contents
- [Module Overview](#module-overview)
- [Module Types](#module-types)
- [Module Structure](#module-structure)
- [Creating a New Module](#creating-a-new-module)
- [Module Template](#module-template)
- [Integration & Registration](#integration--registration)
- [Testing Modules](#testing-modules)
- [Best Practices](#best-practices)
- [Example: Custom Module](#example-custom-module)

## Module Overview

Modules encapsulate specific security tasks (e.g., scanning, exploitation, enumeration). Each module is a Python class that inherits from the base module class and implements required methods.

## Module Types
- **Scanners**: Port, service, and vulnerability scanning
- **Exploits**: Automated exploitation of vulnerabilities
- **Enumeration**: Information gathering
- **Post-Exploitation**: Actions after compromise
- **Social Engineering**: Phishing, pretexting, etc.
- **Brute Force**: Password/authentication testing
- **Custom**: Any user-defined logic

## Module Structure

Modules reside in `src/modules/` and its subdirectories. Each module should:
- Inherit from `BaseModule` (`src/modules/base_module.py`)
- Implement required methods: `run()`, `configure()`, etc.
- Define metadata: name, description, author, options

## Creating a New Module
1. **Copy the template:**
   - Use `data/templates/module_template.py` as a starting point.
2. **Rename and place:**
   - Place your new module in the appropriate subdirectory (e.g., `src/modules/scanners/`).
3. **Edit class and metadata:**
   - Update class name, description, and options.
4. **Implement logic:**
   - Write your module's main logic in the `run()` method.

## Module Template

See `data/templates/module_template.py` for a ready-to-use template. Example skeleton:

```python
from modules.base_module import BaseModule

class MyCustomModule(BaseModule):
    name = "My Custom Module"
    description = "Describe what this module does."
    author = "Your Name"
    options = {
        "target": "Target IP or domain",
        # ... other options ...
    }

    def configure(self, **kwargs):
        # Set options from kwargs
        pass

    def run(self):
        # Main module logic
        pass
```

## Integration & Registration
- Modules are auto-discovered if placed in the correct directory and inherit from `BaseModule`.
- For advanced registration, update `src/core/module_manager.py` if needed.

## Testing Modules
- Place tests in `tests/unit/` or `tests/integration/`.
- Use `pytest` for running tests.
- Mock external dependencies for isolated testing.

## Best Practices
- Keep modules focused and single-purpose.
- Use clear, descriptive names and docstrings.
- Handle errors gracefully and log appropriately.
- Follow PEP8 and project code style.

## Example: Custom Module

See `examples/custom_modules/custom_module_example.py` for a full example.

---

For more details, see:
- [Architecture](architecture.md)
- [Development Guide](index.md)
- [API Documentation](../api/index.md)
