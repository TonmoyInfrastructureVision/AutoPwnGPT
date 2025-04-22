# AutoPwnGPT Project

## Overview

AutoPwnGPT is a next-generation offensive security tool that combines a modular penetration testing framework with a GPT-powered natural language interface. The core concept is elegantly simple yet powerful: **"You type what you want to do — it figures out how to do it and runs the attack steps modularly."**

This tool enables security professionals to conduct comprehensive security assessments using natural language commands, which are automatically translated into technical operations executed by specialized modules.

## Key Features

- **Natural Language Interface**: Use plain English commands to orchestrate complex security operations
- **Modular Execution Engine**: Tasks are broken down into classic pentesting modules (e.g., Nmap, Nikto, Hydra)
- **Contextual Memory**: Maintains state during assessment sessions for multi-step attacks and chaining
- **Payload Generator**: Dynamically creates payloads for various attack scenarios
- **Recon & Exploit Chains**: Suggests and auto-executes post-exploitation steps
- **Reports & Session Logs**: Generates detailed reports with attack paths and findings
- **Offline Mode**: Functions in air-gapped environments using local LLMs
- **PyQt6 GUI**: Modern, intuitive graphical interface for visualizing operations

## Complete Project Structure

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
│   │   ├── __init__.py
│   │   ├── authentication.py # API auth mechanism
│   │   ├── middleware.py     # Request/response processing
│   │   ├── models.py         # API data models
│   │   ├── routes.py         # API endpoints
│   │   └── server.py         # API server implementation
│   │
│   ├── config/               # Configuration management
│   │   ├── __init__.py
│   │   ├── defaults.py       # Default settings
│   │   ├── schema.py         # Config validation schema
│   │   ├── settings.py       # Settings manager
│   │   └── user_config.py    # User configuration
│   │
│   ├── core/                 # Core engine components
│   │   ├── __init__.py
│   │   ├── command_processor.py # Command interpretation
│   │   ├── context_manager.py   # Session context
│   │   ├── engine.py            # Main execution engine
│   │   ├── error_handler.py     # Error management
│   │   ├── logging_system.py    # Logging functionality
│   │   ├── module_manager.py    # Module handling
│   │   ├── session.py           # Session management
│   │   ├── task_scheduler.py    # Task scheduling
│   │   └── workflow_manager.py  # Operation workflows
│   │
│   ├── database/             # Data persistence
│   │   ├── __init__.py
│   │   ├── db_manager.py     # Database connection
│   │   ├── migrations.py     # Schema migrations
│   │   ├── models.py         # ORM models
│   │   └── query_builder.py  # SQL query construction
│   │
│   ├── gui/                  # PyQt6-based interface
│   │   ├── __init__.py
│   │   ├── about_dialog.py   # About information
│   │   ├── console_widget.py # Command console
│   │   ├── dashboard_widget.py # Main dashboard
│   │   ├── main_window.py    # Main application window
│   │   ├── module_browser_widget.py # Module browser
│   │   ├── network_visualizer_widget.py # Target visualization
│   │   ├── report_viewer.py  # Report viewing
│   │   ├── resources.py      # GUI resources
│   │   ├── results_viewer_widget.py # Results display
│   │   ├── session_manager_dialog.py # Session control
│   │   ├── settings_dialog.py # Settings interface
│   │   ├── styles.py         # UI styling
│   │   │
│   │   └── resources/        # GUI assets
│   │       ├── icons/        # Application icons
│   │       │   └── __init__.py
│   │       ├── images/       # Images and graphics
│   │       │   └── __init__.py
│   │       └── themes/       # UI themes
│   │           └── __init__.py
│   │
│   ├── llm_integration/      # AI model integration
│   │   ├── __init__.py
│   │   ├── chain_of_thought.py # Reasoning patterns
│   │   ├── context_builder.py  # Context generation
│   │   ├── gpt_interface.py    # GPT API interface
│   │   ├── llm_manager.py      # LLM control
│   │   ├── local_llm.py        # Local model support
│   │   ├── prompt_templates.py # NL templates
│   │   └── response_parser.py  # LLM response handling
│   │
│   ├── modules/              # Attack modules
│   │   ├── __init__.py
│   │   ├── base_module.py    # Base module class
│   │   ├── brute_force.py    # Authentication attacks
│   │   ├── custom_module_loader.py # Custom module support
│   │   ├── enumeration.py    # Information gathering
│   │   ├── exploit.py        # Exploitation framework
│   │   ├── network.py        # Network operations
│   │   ├── post_exploitation.py # Post-compromise
│   │   ├── scanner.py        # Scanning framework
│   │   ├── social_engineering.py # Human-focused attacks
│   │   ├── web.py            # Web application testing
│   │   ├── wireless.py       # Wireless network testing
│   │   │
│   │   ├── brute_force/      # Brute force modules
│   │   ├── custom/           # Custom modules
│   │   ├── enumeration/      # Enumeration modules
│   │   ├── exploits/         # Exploit modules
│   │   │   ├── __init__.py
│   │   │   ├── buffer_overflow.py  # Buffer overflow exploits
│   │   │   ├── command_injection.py # Command injection exploits  
│   │   │   ├── sql_injection.py     # SQL injection exploits
│   │   │   └── xss.py               # Cross-site scripting exploits
│   │   ├── network/          # Network modules
│   │   ├── post_exploitation/ # Post-exploitation
│   │   ├── scanners/         # Scanner modules
│   │   │   ├── __init__.py
│   │   │   ├── api_scanner.py      # API scanning
│   │   │   ├── network_scanner.py  # Network discovery
│   │   │   ├── port_scanner.py     # Port scanning
│   │   │   ├── vulnerability_scanner.py # Vulnerability scanning
│   │   │   └── web_scanner.py      # Web application scanning
│   │   ├── social_engineering/ # Social engineering modules
│   │   └── wireless/        # Wireless testing modules
│   │
│   ├── payloads/             # Payload generation
│   │   ├── __init__.py
│   │   ├── custom.py         # Custom payload generators
│   │   ├── encoder.py        # Payload encoding
│   │   ├── generator.py      # Payload creation
│   │   ├── shell.py          # Shell payloads
│   │   └── web.py            # Web payloads
│   │
│   ├── reports/              # Report generation
│   │   ├── __init__.py
│   │   ├── exporter.py       # Report export formats
│   │   ├── formatter.py      # Report formatting
│   │   ├── generator.py      # Report creation
│   │   ├── template.py       # Report templates
│   │   └── vulnerability_database.py # Vulnerability info
│   │
│   └── utils/                # Utility functions
│       ├── __init__.py
│       ├── crypto_utils.py   # Cryptographic utilities
│       ├── data_utils.py     # Data manipulation
│       ├── file_utils.py     # File operations
│       ├── network.py        # Network utilities
│       ├── os_utils.py       # OS operations
│       ├── process_utils.py  # Process management
│       ├── security.py       # Security functions
│       ├── string_utils.py   # String manipulation
│       └── validation.py     # Input validation
│
├── data/                     # Data storage
│   ├── logs/                 # Operation logs
│   ├── payloads/             # Generated payloads
│   ├── reports/              # Generated reports
│   ├── sessions/             # Session data
│   ├── templates/            # Templates
│   │   ├── module_template.py  # Module template
│   │   └── report_template.md  # Report template
│   └── wordlists/            # Attack wordlists
│
├── docs/                     # Documentation
│   ├── api/                  # API documentation
│   │   └── index.md
│   ├── development/          # Developer documentation
│   │   ├── architecture.md   # System architecture
│   │   ├── index.md          # Development overview
│   │   └── module_development.md # Module creation guide
│   ├── examples/             # Example documentation
│   ├── index.md              # Documentation index
│   ├── installation.md       # Installation guide
│   └── user_guide/           # User guides
│       └── index.md
│
├── examples/                 # Example usage scenarios
│   ├── advanced/             # Advanced examples
│   │   ├── README.md
│   │   └── advanced_workflow.py
│   ├── basic/                # Basic examples
│   │   ├── README.md
│   │   ├── basic_scan.py
│   │   └── basic_web_scan.py
│   └── custom_modules/       # Custom module examples
│       └── custom_module_example.py
│
├── scripts/                  # Utility scripts
│   ├── build.sh              # Build script
│   ├── install.sh            # Installation script
│   ├── test.sh               # Test runner
│   └── update.sh             # Update script
│
└── tests/                    # Test suites
    ├── conftest.py           # Test configuration
    ├── functional/           # Functional tests
    │   └── __init__.py
    ├── integration/          # Integration tests
    │   ├── __init__.py
    │   └── test_workflows.py
    └── unit/                 # Unit tests
        ├── __init__.py
        ├── test_core.py      # Core component tests
        ├── test_llm.py       # LLM integration tests
        └── test_modules.py   # Module tests
```

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

### Utilities and Support Systems

- **Database**: Persistent storage for scan results, vulnerabilities, and session data
- **Reports**: Generation of comprehensive security assessment reports
- **API**: RESTful interface for programmatic access and integration
- **Config**: Configuration management for application settings and preferences
- **Payloads**: Generation of attack payloads for various attack scenarios

## Security & Ethics

AutoPwnGPT is designed strictly for authorized penetration testing and red team assessments. It includes:
- Terms-of-use enforcement
- Comprehensive audit logging
- Target scope enforcement
- Usage watermarking

## Tech Stack

- **Frontend**: PyQt6
- **Core Engine**: Python 3, asyncio
- **LLM Integration**: OpenAI API, local models (Ollama/LM Studio)
- **Tool Integration**: Standard security tools (Nmap, etc.)
- **Storage**: SQLite for data persistence

## Installation

[Installation instructions will be added here]

## Usage

[Usage examples will be added here]

## Contributing

[Contribution guidelines will be added here]

## License

[License information will be added here]