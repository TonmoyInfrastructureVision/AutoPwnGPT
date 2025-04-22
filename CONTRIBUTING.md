# Contributing to AutoPwnGPT

Thank you for your interest in contributing to AutoPwnGPT! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
- Check the issue tracker to see if the issue has already been reported
- Collect information about your environment (OS, Python version, etc.)
- Provide detailed steps to reproduce the issue

When submitting a bug report, please use the bug report template provided in the issue tracker.

### Suggesting Enhancements

Enhancement suggestions are welcome! When submitting an enhancement suggestion:
- Provide a clear description of the proposed feature
- Explain why the enhancement would be useful
- Consider including mock-ups or examples of how the feature would work

### Code Contributions

#### Setting Up Development Environment

1. Fork the repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/AutoPwnGPT.git
   cd AutoPwnGPT
   ```
3. Set up the development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

#### Development Workflow

1. Create a branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes, following the coding conventions
3. Write/update tests to cover your changes
4. Run tests to ensure they pass:
   ```bash
   pytest
   ```
5. Commit your changes using descriptive commit messages
6. Push your branch to your fork
7. Submit a pull request

#### Pull Request Guidelines

- Fill in the required pull request template
- Include tests for new features or bug fixes
- Update documentation for any changed functionality
- Ensure all tests pass
- Ensure code follows the project's style guidelines

## Coding Standards

- Follow PEP 8 style guidelines
- Write docstrings for all functions, classes, and modules
- Maintain test coverage for all code
- Use type hints where appropriate

## Module Development

If you're contributing a new module:

1. Use the module template in `data/templates/module_template.py`
2. Document the module's purpose, inputs, and outputs
3. Include tests that verify the module works correctly
4. Update the module index in the documentation

## Documentation

- Update documentation for any changed functionality
- Document new features thoroughly
- Fix documentation errors if found

## License

By contributing to AutoPwnGPT, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

---

Author: Eshan Roy  
Email: m.eshanized@gmail.com  
GitHub: https://github.com/TonmoyInfrastructureVision
