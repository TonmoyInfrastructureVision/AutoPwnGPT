# AutoPwnGPT Development Guide

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision
# Date: 2025-04-23

---

Welcome to the AutoPwnGPT development documentation. This guide is intended for contributors and developers who want to understand, extend, or improve the AutoPwnGPT framework.

## Table of Contents

- [Project Structure](../development/architecture.md)
- [Development Environment Setup](#development-environment-setup)
- [Core Concepts](#core-concepts)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [Code Style & Guidelines](#code-style--guidelines)
- [Contributing](#contributing)
- [Module Development](module_development.md)

## Development Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TonmoyInfrastructureVision/AutoPwnGPT.git
   cd AutoPwnGPT
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```
4. **Run tests:**
   ```bash
   pytest
   ```

## Core Concepts

- **Modular Design:** Each security function is implemented as a module. Modules are easy to add, remove, or update.
- **Natural Language Processing:** The LLM integration translates user intent into actionable steps.
- **Extensible Engine:** The core engine manages workflow, context, and module orchestration.
- **GUI/CLI/API:** Multiple interfaces for different user needs.

## Adding New Features

- Review the [architecture documentation](architecture.md) to understand where your feature fits.
- Follow the code style and contribution guidelines.
- Add or update tests for your feature.
- Document your changes in the code and update relevant docs.

## Testing

- Unit tests are in `tests/unit/`
- Integration tests are in `tests/integration/`
- Use `pytest` to run all tests.
- Ensure all tests pass before submitting a pull request.

## Code Style & Guidelines

- Follow PEP8 for Python code.
- Use descriptive commit messages.
- Add docstrings and comments where necessary.
- See [CONTRIBUTING.md](../../CONTRIBUTING.md) for more details.

## Contributing

- Fork the repository and create a feature branch.
- Make your changes and commit them with clear messages.
- Push to your fork and submit a pull request.
- Fill out the PR template and link any relevant issues.

## Resources

- [Architecture](architecture.md)
- [Module Development](module_development.md)
- [API Documentation](../api/index.md)
- [User Guide](../user_guide/index.md)

---

For any questions, join our [Discord](https://discord.gg/autopwngpt) or open an issue on GitHub.
