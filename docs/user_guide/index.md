# User Guide

This user guide provides detailed information on how to use AutoPwnGPT effectively for security assessments.

## Table of Contents

- [Getting Started](#getting-started)
- [Command Syntax](#command-syntax)
- [GUI Interface](#gui-interface)
- [Modules](#modules)
- [Workflows](#workflows)
- [Report Generation](#report-generation)
- [Troubleshooting](#troubleshooting)

## Getting Started

To get started with AutoPwnGPT, first ensure you have completed the [installation](../installation.md) process.

### Basic Usage

Launch AutoPwnGPT using:

```bash
# GUI mode
python src/main.py

# CLI mode
python src/cli.py
```

### First Commands

Try these basic commands to familiarize yourself with the system:

```
# Basic network scan
scan network 192.168.1.0/24

# Web application assessment
analyze website https://example.com

# Help command
help
```

## Command Syntax

AutoPwnGPT understands natural language commands, but follows certain patterns for better results:

### Basic Command Structure

```
<action> <target> [options]
```

Examples:
- `scan network 192.168.1.0/24`
- `find vulnerabilities on 192.168.1.10`
- `brute force ssh on 192.168.1.15 using wordlist common-passwords.txt`

### Context Awareness

AutoPwnGPT maintains context between commands, allowing you to refer to previous results:

```
scan network 192.168.1.0/24
analyze the web server on the third host
```

## GUI Interface

The graphical user interface provides an intuitive way to interact with AutoPwnGPT.

### Main Components

- **Command Console**: Central input area for commands
- **Dashboard**: Overview of current assessment status
- **Network Visualizer**: Visual representation of discovered hosts
- **Module Browser**: Access to available modules
- **Results Viewer**: Display area for scan results
- **Report Viewer**: For viewing and exporting reports

### Keyboard Shortcuts

- `Ctrl+N`: New session
- `Ctrl+S`: Save session
- `Ctrl+O`: Open session
- `Ctrl+R`: Run command
- `Ctrl+L`: Clear console
- `F1`: Help

## Modules

AutoPwnGPT is built on a modular framework where each security function is provided by a specialized module.

### Core Modules

- **Network Scanner**: Discovers hosts and open ports
- **Vulnerability Scanner**: Identifies security issues
- **Web Scanner**: Tests web applications for vulnerabilities
- **Brute Force**: Password testing against various services
- **Exploit**: Execution of exploits against vulnerable targets
- **Post-Exploitation**: Actions after successful compromise

### Using Modules Directly

While natural language is the primary interface, you can also call modules directly:

```
run module network_scanner --target 192.168.1.0/24 --ports 1-1000
```

## Workflows

Workflows allow you to chain multiple operations into a sequence.

### Creating Workflows

```
create workflow web_assessment
add step "scan network 192.168.1.0/24"
add step "identify web servers"
add step "run vulnerability scan on each web server"
add step "generate report"
save workflow
```

### Running Workflows

```
run workflow web_assessment --target 192.168.1.0/24
```

## Report Generation

AutoPwnGPT can generate comprehensive reports of your security assessments.

### Basic Report

```
generate report
```

### Customized Reports

```
generate report --format pdf --include-evidence --risk-level high
```

## Troubleshooting

For common issues and their solutions, see the [Troubleshooting Guide](troubleshooting.md).

---

Author: Eshan Roy  
Email: m.eshanized@gmail.com  
GitHub: https://github.com/TonmoyInfrastructureVision
