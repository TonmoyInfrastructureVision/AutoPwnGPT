# AutoPwnGPT

<div align="center">

```
    _         _        ____                  ____ ____ _____
   / \  _   _| |_ ___ |  _ \__      ___ __ / ___|  _ \_   _|
  / _ \| | | | __/ _ \| |_) \ \ /\ / / '_ \ |  _| |_) || |
 / ___ \ |_| | || (_) |  __/ \ V  V /| | | | |__|  __/ | |
/_/   \_\__,_|\__\___/|_|     \_/\_/ |_| |_|\____|_|    |_|
```

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/TonmoyInfrastructureVision/AutoPwnGPT?style=social)](https://github.com/TonmoyInfrastructureVision/AutoPwnGPT/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/TonmoyInfrastructureVision/AutoPwnGPT)](https://github.com/TonmoyInfrastructureVision/AutoPwnGPT/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/TonmoyInfrastructureVision/AutoPwnGPT/pulls)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/TonmoyInfrastructureVision/AutoPwnGPT/graphs/commit-activity)

<br>
<img src="https://img.shields.io/badge/Security-Offensive-red.svg">
<img src="https://img.shields.io/badge/AI-Powered-blue.svg">
<img src="https://img.shields.io/badge/LLM-Integration-purple.svg">
<img src="https://img.shields.io/badge/Modular-Framework-orange.svg">
<br><br>

<h3>🧠 Natural Language Penetration Testing Framework</h3>
<i>You type what you want to do — it figures out how to do it and runs the attack steps modularly</i>

[🚀 Features](#key-features) • [⚡️ Quick Start](#quick-start) • [📘 Documentation](#documentation) • [🛠️ Examples](#examples) • [🤝 Contributing](#contributing)

---

<img src="https://raw.githubusercontent.com/TonmoyInfrastructureVision/AutoPwnGPT/main/docs/images/dashboard-preview.png" alt="AutoPwnGPT Dashboard" width="800"/>

</div>

## 🎯 Overview

AutoPwnGPT is a next-generation offensive security tool that combines a modular penetration testing framework with a GPT-powered natural language interface. The core concept is elegantly simple yet powerful: **"You type what you want to do — it figures out how to do it and runs the attack steps modularly."**

This tool enables security professionals to conduct comprehensive security assessments using natural language commands, which are automatically translated into technical operations executed by specialized modules.

<!-- <div align="center">
<img src="https://imgur.com/placeholder-for-screenshot.png" alt="AutoPwnGPT Screenshot" width="800"/>
</div> -->

## Key Features

- **🧠 Natural Language Interface**: Use plain English commands to orchestrate complex security operations
- **🧩 Modular Execution Engine**: Tasks are broken down into classic pentesting modules (e.g., Nmap, Nikto, Hydra)
- **🧿 Contextual Memory**: Maintains state during assessment sessions for multi-step attacks and chaining
- **💣 Payload Generator**: Dynamically creates payloads for various attack scenarios
- **🔄 Recon & Exploit Chains**: Suggests and auto-executes post-exploitation steps
- **📊 Reports & Session Logs**: Generates detailed reports with attack paths and findings
- **🔌 Offline Mode**: Functions in air-gapped environments using local LLMs
- **🖥️ PyQt6 GUI**: Modern, intuitive graphical interface for visualizing operations

## Installation

### Prerequisites

- Python 3.10 or higher
- Git
- [Optional] Docker for containerized deployment

### Option 1: Direct Installation

```bash
# Clone the repository
git clone https://github.com/TonmoyInfrastructureVision/AutoPwnGPT.git
cd AutoPwnGPT

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### Option 2: Docker Installation

```bash
# Clone the repository
git clone https://github.com/TonmoyInfrastructureVision/AutoPwnGPT.git
cd AutoPwnGPT

# Build and run with Docker Compose
docker-compose up -d

# Access the application at http://localhost:8080
```

### Option 3: Install via Script

```bash
curl -sSL https://raw.githubusercontent.com/TonmoyInfrastructureVision/AutoPwnGPT/main/scripts/install.sh | bash
```

## Quick Start

```python
# Launch the GUI
python src/main.py

# Or use the CLI
python src/cli.py "scan the target 192.168.1.10 for open ports and vulnerabilities"
```

## Project Structure

```
AutoPwnGPT/
├── CHANGELOG.md              # Version history and changes
├── CODE_OF_CONDUCT.md        # Community guidelines
├── CONTRIBUTING.md           # Contribution guidelines
├── Dockerfile                # Container definition
├── LICENSE                   # Project license
├── README.md                 # This file
├── config.yaml               # Default configuration
├── docker-compose.yml        # Docker environment setup
├── requirements-dev.txt      # Development dependencies
├── requirements.txt          # Production dependencies
├── setup.py                  # Package installation script
├── .dockerignore             # Docker build exclusions
├── .env.example              # Environment variables template
├── .gitattributes            # Git file attributes
├── .gitignore                # Git ignore patterns  
│
├── src/                      # Main source code directory
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── main.py               # Application entry point
│   ├── version.py            # Version information
│   │
│   ├── api/                  # REST API for integrations
│   ├── config/               # Configuration management
│   ├── core/                 # Core engine components
│   ├── database/             # Data persistence
│   ├── gui/                  # PyQt6-based interface
│   ├── llm_integration/      # AI model integration
│   ├── modules/              # Attack modules
│   ├── payloads/             # Payload generation
│   ├── reports/              # Report generation
│   └── utils/                # Utility functions
│
├── data/                     # Data storage
├── docs/                     # Documentation
├── examples/                 # Example usage scenarios
├── scripts/                  # Utility scripts
└── tests/                    # Test suites
```

For a complete directory structure, see the [Project Structure Documentation](docs/development/architecture.md).

## Component Explanations

### Core System

The core system is the brain of AutoPwnGPT, responsible for:
- **Command Processor**: Parses natural language commands and determines intent
- **Engine**: Coordinates the execution of modules based on commands
- **Module Manager**: Loads, configures, and runs the appropriate modules
- **Session Management**: Maintains state and context during assessments
- **Workflow Manager**: Handles multi-step operation sequences
- **Context Manager**: Manages the contextual understanding of target environments

### Modules

Modules are the workhorses that perform specific security testing functions:
- **Scanners**: Identify targets and vulnerabilities (port scanning, service enumeration)
- **Exploits**: Execute attacks against discovered vulnerabilities (SQL injection, XSS, buffer overflows)
- **Enumeration**: Gather detailed information about targets (directories, users, technologies)
- **Post-Exploitation**: Actions after successful compromise (privilege escalation, lateral movement)
- **Social Engineering**: User-targeted attack vectors (phishing, pretexting)
- **Brute Force**: Password and authentication testing

### LLM Integration

The AI integration layer translates between natural language and technical operations:
- **GPT Interface**: Communication with OpenAI's GPT models
- **Local LLM**: Support for offline operation using local models
- **Prompt Templates**: Structured templates for consistent LLM interaction
- **Response Parser**: Interprets and structures LLM responses
- **Context Builder**: Creates context for better LLM understanding of the security environment
- **Chain of Thought**: Implements reasoning patterns for complex security decisions

### GUI Interface

The PyQt6-based interface provides:
- **Main Window**: Primary application container
- **Console Widget**: Command entry and interaction
- **Dashboard Widget**: Overview of system status and recent activities
- **Network Visualizer**: Visual representation of discovered network topology
- **Module Browser**: Exploration and manual selection of modules
- **Results Viewer**: Display of operation results and findings
- **Report Viewer**: Interactive report viewing and export

## Security & Ethics

AutoPwnGPT is designed strictly for authorized penetration testing and red team assessments. It includes:
- Terms-of-use enforcement
- Comprehensive audit logging
- Target scope enforcement
- Usage watermarking

**⚠️ IMPORTANT:** This tool should only be used against systems you own or have explicit permission to test. Unauthorized use is illegal and unethical.

## Tech Stack

- **Frontend**: PyQt6
- **Core Engine**: Python 3, asyncio
- **LLM Integration**: OpenAI API, local models (Ollama/LM Studio)
- **Tool Integration**: Standard security tools (Nmap, etc.)
- **Storage**: SQLite for data persistence

## Documentation

Complete documentation is available in the [docs](docs/) directory:

- [Installation Guide](docs/installation.md)
- [User Guide](docs/user_guide/index.md)
- [API Documentation](docs/api/index.md)
- [Developer Guide](docs/development/index.md)
- [Module Development](docs/development/module_development.md)

## Examples

Check out these examples to get started:

- [Basic Scan](examples/basic/basic_scan.py): Simple target scanning
- [Web Application Assessment](examples/basic/basic_web_scan.py): Web application security testing
- [Advanced Workflow](examples/advanced/advanced_workflow.py): Complex multi-stage operations
- [Custom Module Development](examples/custom_modules/custom_module_example.py): Creating your own modules

## Roadmap

- [ ] Integration with additional security tools
- [ ] Enhanced reporting with interactive visualizations
- [ ] Support for collaborative team-based assessments
- [ ] Advanced exploit development capabilities
- [ ] Cloud-based deployment options
- [ ] Mobile application testing modules

## Contributing

We welcome contributions from the security community! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/TonmoyInfrastructureVision/AutoPwnGPT.git
cd AutoPwnGPT

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

## Community

- [Discord](https://discord.gg/autopwngpt)
- [Twitter](https://twitter.com/autopwngpt)
- [Blog](https://autopwngpt.com/blog)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Eshan Roy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

## Acknowledgements

- [OpenAI](https://openai.com/) for GPT technology
- The open-source security tools community
- All contributors who have helped shape this project

---

<div align="center">
  <sub>Built with ❤️ by the security community</sub>
</div>