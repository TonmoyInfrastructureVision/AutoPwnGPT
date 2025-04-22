# Installation Guide

This guide provides detailed instructions for installing AutoPwnGPT on various platforms.

## Prerequisites

Before installing AutoPwnGPT, ensure that you have the following prerequisites installed:

- Python 3.10 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)

For certain modules, you may also need:
- Required system packages for specific penetration testing tools
- Docker (optional, for containerized deployment)

## Method 1: Standard Installation

The standard installation is recommended for most users and provides the full functionality of AutoPwnGPT.

```bash
# Clone the repository
git clone https://github.com/TonmoyInfrastructureVision/AutoPwnGPT.git
cd AutoPwnGPT

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python src/main.py --version
```

## Method 2: Development Installation

If you plan to contribute to the project or develop custom modules, use the development installation.

```bash
# Clone the repository
git clone https://github.com/TonmoyInfrastructureVision/AutoPwnGPT.git
cd AutoPwnGPT

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests to verify installation
pytest
```

## Method 3: Docker Installation

For isolated deployment or if you prefer containerization:

```bash
# Clone the repository
git clone https://github.com/TonmoyInfrastructureVision/AutoPwnGPT.git
cd AutoPwnGPT

# Build and run with Docker Compose
docker-compose up -d

# Access the application at http://localhost:8080
```

## Method 4: Installation Script

For quick setup, you can use our installation script:

```bash
curl -sSL https://raw.githubusercontent.com/TonmoyInfrastructureVision/AutoPwnGPT/main/scripts/install.sh | bash
```

## Configuration

After installation, you should configure AutoPwnGPT by editing the `config.yaml` file to suit your needs:

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration with your preferred editor
nano config.yaml
```

### API Keys

If you plan to use OpenAI's GPT models, you'll need to set your API key:

```yaml
# In config.yaml
llm:
  provider: "openai"
  api_key: "your-api-key-here"
  model_name: "gpt-4"
```

For local models, configure the local endpoint:

```yaml
# In config.yaml
llm:
  provider: "local"
  endpoint: "http://localhost:8000/v1"
  model_name: "local-model"
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: If you encounter errors about missing packages, ensure you've installed all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Permission Issues**: If you encounter permission errors during installation:
   ```bash
   pip install --user -r requirements.txt
   ```

3. **Docker Issues**: If Docker container fails to start, check logs:
   ```bash
   docker-compose logs
   ```

### Getting Help

If you encounter issues not covered in this guide:

- Check the [Troubleshooting](user_guide/troubleshooting.md) section
- Open an issue on GitHub
- Join our community Discord server for real-time assistance

---

Author: Eshan Roy  
Email: m.eshanized@gmail.com  
GitHub: https://github.com/TonmoyInfrastructureVision
