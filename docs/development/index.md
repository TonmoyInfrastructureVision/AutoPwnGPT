# Development Guide

This guide is intended for developers who want to contribute to AutoPwnGPT, extend its functionality, or understand how it works internally.

## Table of Contents

- [Architecture Overview](architecture.md)
- [Development Environment Setup](#development-environment)
- [Coding Standards](#coding-standards)
- [Module Development](module_development.md)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Development Environment

### Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/AutoPwnGPT.git
cd AutoPwnGPT
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Development Tools

The project uses several tools to maintain code quality:

- **Black**: For code formatting
- **Pylint**: For static code analysis
- **MyPy**: For type checking
- **Pytest**: For testing
- **Pre-commit hooks**: To enforce standards before committing

You can run these tools with:

```bash
# Format code
black src/ tests/

# Check code quality
pylint src/ tests/

# Type checking
mypy src/

# Run tests
pytest
```

## Coding Standards

We follow these coding standards:

1. **PEP 8**: For code style
2. **Type Hints**: Always use type hints for function parameters and return values
3. **Docstrings**: All modules, classes, and functions should have docstrings
4. **Comments**: Add comments for complex logic
5. **Error Handling**: Use proper error handling and avoid bare exceptions
6. **Logging**: Use the logging system instead of print statements

Example:

```python
def scan_network(target: str, port_range: str = "1-1000") -> Dict[str, Any]:
    """
    Scan a network target for open ports.
    
    Args:
        target: The IP address or network range to scan (e.g., 192.168.1.1 or 192.168.1.0/24)
        port_range: The range of ports to scan (default: "1-1000")
        
    Returns:
        A dictionary containing scan results with hosts and open ports
        
    Raises:
        NetworkScanError: If the scan fails
    """
    # Implementation
```

## Testing

### Writing Tests

Tests should be written for all functionality:

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test how components work together
3. **Functional Tests**: Test complete workflows

Tests should be placed in the `tests/` directory with a structure mirroring the `src/` directory.

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_module_manager.py

# Run with coverage report
pytest --cov=src tests/
```

## Documentation

Documentation should be written in Markdown and placed in the `docs/` directory.

### Documentation Structure

- User-facing documentation in `docs/user_guide/`
- API documentation in `docs/api/`
- Developer documentation in `docs/development/`

## Pull Request Process

1. Create a new branch from `main`
2. Make your changes
3. Ensure tests pass and code meets standards
4. Update documentation if necessary
5. Submit a pull request
6. Respond to review comments

See the [Contributing Guide](../contributing.md) for more details on the contribution process.

---

Author: Eshan Roy  
Email: m.eshanized@gmail.com  
GitHub: https://github.com/TonmoyInfrastructureVision
