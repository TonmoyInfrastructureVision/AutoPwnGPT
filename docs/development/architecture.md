# AutoPwnGPT Architecture

Author: Eshan Roy
Email: m.eshanized@gmail.com
GitHub: https://github.com/TonmoyInfrastructureVision
Date: 2025-04-22

## System Overview

AutoPwnGPT is an offensive security tool that combines a modular penetration testing framework with GPT-powered natural language processing. The architecture follows a layered approach with clear separation of concerns between components.

## Core Components

### 1. Natural Language Interface
- **Command Processor**: Translates natural language input into structured commands
- **Context Manager**: Maintains session context for multi-step operations
- **Response Formatter**: Formats technical results into human-readable output

### 2. Core Engine
- **Engine**: Central coordinator managing workflow execution
- **Module Manager**: Handles module discovery, loading, and execution
- **Task Scheduler**: Manages asynchronous task execution
- **Session Manager**: Maintains stateful sessions for ongoing operations
- **Error Handler**: Provides unified error handling and recovery mechanisms
- **Logging System**: Comprehensive logging for operations and debugging

### 3. LLM Integration
- **GPT Interface**: Communicates with OpenAI's GPT API
- **Local LLM**: Supports offline operation with local models
- **Prompt Templates**: Pre-defined templates for security operations
- **Chain of Thought**: Implements reasoning patterns for complex security decisions
- **Context Builder**: Creates context for better LLM understanding
- **Response Parser**: Interprets LLM responses into actionable instructions

### 4. Module System
- **Base Module**: Abstract class defining module interface
- **Module Categories**:
  - Scanners (port, network, web, vulnerability)
  - Exploits (SQL injection, XSS, command injection, etc.)
  - Enumeration (directories, subdomains, services)
  - Post-Exploitation (privilege escalation, lateral movement)
  - Brute Force (password testing, authentication attacks)
  - Social Engineering (phishing, pretexting)
- **Custom Module Loader**: Support for user-created modules

### 5. Database
- **DB Manager**: Database connection and transaction management
- **ORM Models**: Object-relational mapping for data entities
- **Query Builder**: SQL query construction and execution
- **Migrations**: Schema evolution and management

### 6. User Interfaces
- **CLI**: Command-line interface for terminal operation
- **GUI**: PyQt6-based graphical interface:
  - Main Window: Application container
  - Console Widget: Command entry point
  - Dashboard: System status overview
  - Module Browser: Module exploration and selection
  - Results Viewer: Display of operation results
  - Network Visualizer: Visual representation of discovered network

### 7. Reporting System
- **Report Generator**: Creates detailed security assessment reports
- **Report Templates**: Customizable report templates
- **Exporters**: Support for various output formats (PDF, HTML, Markdown)
- **Vulnerability Database**: Information about known vulnerabilities

### 8. Utilities
- **File Utils**: File system operations
- **Network Utils**: Network-related utilities
- **Crypto Utils**: Cryptographic operations
- **Data Utils**: Data manipulation helpers
- **Process Utils**: Process management utilities
- **OS Utils**: Operating system interactions
- **Security Utils**: Security-related helper functions

## Data Flow

1. **User Input Flow**:
   - User enters natural language command
   - Command Processor parses input using LLM
   - Engine identifies required modules
   - Module Manager loads and executes modules
   - Results are processed and presented to user

2. **Module Execution Flow**:
   - Module Manager loads required module
   - Dependencies are resolved
   - Pre-execution validation
   - Module execution
   - Result collection and processing
   - Context updating with findings

3. **Reporting Flow**:
   - Findings collected from modules
   - Data aggregated and analyzed
   - Report template selected/customized
   - Report generated in selected format
   - Report presented to user or exported

## Security Considerations

- **Scope Enforcement**: Ensures operations remain within authorized scope
- **Credential Handling**: Secure storage and handling of authentication credentials
- **Audit Logging**: Comprehensive logging of all operations for accountability
- **Watermarking**: Attribution of actions for tracking
- **Data Protection**: Secure handling of sensitive findings and data

## Extensibility

The system is designed for extensibility through:
- Modular architecture allowing easy addition of new modules
- Plugin system for extending core functionality
- Custom module development SDK
- API for integration with other security tools

## Implementation Notes

- Asynchronous operations using Python's asyncio
- Typed interfaces using Python type hints
- Comprehensive test coverage
- Clear error handling and graceful degradation
- Configuration-driven behavior for flexibility
