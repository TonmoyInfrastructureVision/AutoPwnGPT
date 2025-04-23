# AutoPwnGPT Architecture

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision
# Date: 2025-04-23

---

## Overview

AutoPwnGPT is a modular, AI-powered penetration testing framework that enables users to perform security assessments using natural language commands. The system translates user intent into technical operations, orchestrating a suite of classic and modern security modules through a robust, extensible architecture.

## High-Level Architecture

```
+-------------------+         +-------------------+         +-------------------+
|  User Interface   | <-----> |   Core Engine     | <-----> |    Modules        |
| (GUI/CLI/API/LLM) |         | (Orchestration)   |         | (Scanners, etc.)  |
+-------------------+         +-------------------+         +-------------------+
        |                           |                               |
        v                           v                               v
+-------------------+     +-------------------+         +-------------------+
|  LLM Integration  |     |  Context Manager  |         |  Data/Reports     |
+-------------------+     +-------------------+         +-------------------+
```

- **User Interface**: Accepts natural language or technical commands via GUI (PyQt6), CLI, or API.
- **Core Engine**: Parses, interprets, and orchestrates tasks, managing workflow, context, and session state.
- **Modules**: Pluggable components for scanning, exploitation, enumeration, post-exploitation, etc.
- **LLM Integration**: Bridges natural language and technical actions using GPT or local LLMs.
- **Context Manager**: Maintains assessment state, target information, and session memory.
- **Data/Reports**: Handles persistence, reporting, and audit logging.

## Directory Structure

See the [README.md](../../README.md#project-structure) for a visual directory tree. Key directories:

- `src/`: Main application code (core engine, modules, GUI, LLM integration, etc.)
- `docs/`: Documentation (user, API, developer, module development)
- `examples/`: Usage and module examples
- `data/`: Storage for logs, payloads, reports, sessions
- `scripts/`: Utility scripts for setup, testing, etc.
- `tests/`: Unit, integration, and functional tests

## Core Components

### 1. Core System
- **Command Processor**: Parses user input and determines intent.
- **Engine**: Orchestrates module execution and workflow.
- **Module Manager**: Loads, configures, and runs modules.
- **Session Management**: Maintains state/context for multi-step operations.
- **Workflow Manager**: Handles complex, chained attack sequences.
- **Context Manager**: Tracks targets, environment, and session data.

### 2. Modules
- **Scanners**: Port, service, and vulnerability scanning.
- **Exploits**: Automated exploitation of discovered vulnerabilities.
- **Enumeration**: Information gathering (users, directories, tech stack).
- **Post-Exploitation**: Privilege escalation, lateral movement, persistence.
- **Social Engineering**: Phishing, pretexting, and other user-focused attacks.
- **Brute Force**: Password and authentication testing.

### 3. LLM Integration
- **GPT Interface**: Connects to OpenAI or other LLM APIs.
- **Local LLM**: Supports offline operation with local models.
- **Prompt Templates**: Ensures consistent, structured LLM queries.
- **Response Parser**: Converts LLM output into actionable steps.
- **Context Builder**: Provides context for LLM to improve accuracy.
- **Chain of Thought**: Implements reasoning for complex decisions.

### 4. GUI (PyQt6)
- **Main Window**: Application container.
- **Console Widget**: Command entry and feedback.
- **Dashboard Widget**: System status and activity overview.
- **Network Visualizer**: Visualizes discovered network topology.
- **Module Browser**: Explore and select modules.
- **Results/Report Viewer**: View and export findings.

### 5. Data & Reporting
- **Database**: SQLite for session, result, and log storage.
- **Reports**: Automated generation of assessment reports.
- **Audit Logging**: Tracks all actions for compliance and review.

## Security & Ethics

- **Terms-of-use enforcement**
- **Audit logging**
- **Target scope enforcement**
- **Usage watermarking**

**IMPORTANT:** Use only on systems you own or have explicit permission to test.

## Extensibility

- **Module System**: Easily add new scanners, exploits, or integrations.
- **LLM Abstraction**: Swap between OpenAI and local LLMs.
- **API**: RESTful API for automation and integration.
- **GUI/CLI**: Both graphical and command-line interfaces supported.

## Data Flow Example

1. User enters a natural language command (GUI/CLI/API).
2. Command Processor parses intent and context.
3. Engine determines required modules and workflow.
4. Modules execute tasks, results are stored and visualized.
5. LLM assists with translation, reasoning, and chaining steps.
6. Reports and logs are generated for review.

---

For more details, see:
- [User Guide](../user_guide/index.md)
- [Module Development](module_development.md)
- [API Documentation](../api/index.md)
- [README.md](../../README.md)
