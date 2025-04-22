# Troubleshooting Guide

This guide helps you resolve common issues that may arise when using AutoPwnGPT.

## Common Issues and Solutions

### Installation Issues

#### Missing Dependencies

**Problem**: Error messages about missing packages or dependencies.

**Solution**:
```bash
# Update pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# For system dependencies (on Debian/Ubuntu)
sudo apt-get update
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
```

#### Permission Errors

**Problem**: Permission denied errors during installation.

**Solution**:
```bash
# Install for current user only
pip install --user -r requirements.txt

# Or use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Startup Issues

#### Module Import Errors

**Problem**: The application fails to start with import errors.

**Solution**:
1. Ensure you're in the project root directory
2. Activate the virtual environment
3. Verify that all dependencies are installed
4. Check for any syntax errors in custom modules

```bash
# Verify the environment
which python
pip list

# Try running with verbose output
python -v src/main.py
```

#### Configuration Errors

**Problem**: The application fails to start due to configuration errors.

**Solution**:
1. Check your `config.yaml` file for syntax errors
2. Compare with the example configuration
3. Reset to default configuration if needed

```bash
# Copy the default configuration
cp config.yaml.example config.yaml
```

### API Issues

#### Authentication Errors

**Problem**: Unable to authenticate with the API.

**Solution**:
1. Verify your API key is correct
2. Check that the API key is properly included in the `X-API-Key` header
3. Generate a new API key if needed

```bash
# Generate a new API key
python src/cli.py --generate-api-key
```

#### Rate Limiting

**Problem**: Receiving 429 Too Many Requests responses.

**Solution**:
1. Implement exponential backoff in your API requests
2. Reduce the frequency of requests
3. Check the response headers for rate limit information

### Module Execution Issues

#### Hanging Operations

**Problem**: Modules or commands seem to hang or never complete.

**Solution**:
1. Check network connectivity to the target
2. Verify firewall settings aren't blocking traffic
3. Set shorter timeouts in the configuration
4. Check system resource usage

```bash
# Cancel the current operation
Ctrl+C

# Check system resources
top
```

#### Module Errors

**Problem**: Specific modules fail with errors.

**Solution**:
1. Check module-specific documentation
2. Verify that required external tools are installed
3. Look for error messages in the logs
4. Try running with increased logging level

```bash
# Run with debug logging
python src/main.py --log-level DEBUG
```

### LLM Integration Issues

#### API Key Issues

**Problem**: Error connecting to OpenAI or other LLM provider.

**Solution**:
1. Verify your API key is correct in `config.yaml`
2. Check your internet connection
3. Verify that the API endpoint is accessible
4. Check if you've exceeded your API quota

#### Local LLM Issues

**Problem**: Issues with local LLM models.

**Solution**:
1. Verify the local LLM service is running
2. Check the endpoint configuration
3. Ensure your system has enough resources
4. Try a smaller model if resources are limited

```bash
# Check if the local LLM service is running
curl http://localhost:8000/v1/models
```

### GUI Issues

#### Interface Not Responding

**Problem**: The GUI becomes unresponsive or crashes.

**Solution**:
1. Restart the application
2. Check system resources
3. Update PyQt6 components
4. Try running with the `--no-gui` option to use CLI mode

```bash
# Run in CLI mode
python src/cli.py
```

#### Display Problems

**Problem**: GUI elements are misaligned or not showing properly.

**Solution**:
1. Update to the latest version
2. Check your screen resolution and scaling settings
3. Try resetting the GUI layout

```bash
# Reset GUI settings
python src/main.py --reset-gui-config
```

## Logging and Diagnostics

### Enabling Debug Logging

Increase logging verbosity to get more information:

```bash
python src/main.py --log-level DEBUG
```

### Checking Log Files

Log files can provide valuable information for troubleshooting:

```bash
# View the last 50 lines of the log
tail -n 50 data/logs/autopwngpt.log

# Search for error messages
grep -i error data/logs/autopwngpt.log
```

### Diagnostic Tools

The application includes built-in diagnostic tools:

```bash
# Run system checks
python src/cli.py --system-check

# Test module functionality
python src/cli.py --test-module network_scanner
```

## Getting Help

If you're still experiencing issues:

1. Check the [GitHub Issues](https://github.com/TonmoyInfrastructureVision/AutoPwnGPT/issues) for similar problems
2. Search the [Documentation](../index.md) for more information
3. Join our [Discord community](https://discord.gg/autopwngpt) for real-time help
4. Open a new issue with detailed information about your problem

When reporting issues, please include:
- AutoPwnGPT version
- Operating system and version
- Python version
- Relevant log entries
- Steps to reproduce the issue

---

Author: Eshan Roy  
Email: m.eshanized@gmail.com  
GitHub: https://github.com/TonmoyInfrastructureVision 