#!/bin/bash
# AutoPwnGPT Installation Script

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision

set -e

# ANSI color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "  _____         _        _____                 _____ _____ _____ "
echo " |  _  |_ _ ___| |_ ___ |  _  |_ _ ___ ___ ___|  _  |_   _|_   _|"
echo " |     | | |  _| . | . ||   __| | |   |   | . |   __|_| |_  | |  "
echo " |__|__|___|_| |___|  _||__|  |___|_|_|_|_|___|__|    |_|   |_|  "
echo "                   |_|                                            "
echo -e "${NC}"
echo -e "${GREEN}AutoPwnGPT Installation Script${NC}"
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
  echo -e "${YELLOW}Warning: This script is running as root. It's recommended to install as a regular user.${NC}"
  read -p "Continue as root? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Function to check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check system dependencies
echo -e "${BLUE}Checking system dependencies...${NC}"

# Check Python version
if ! command_exists python3; then
  echo -e "${RED}Python 3 is not installed. Please install Python 3.10 or higher.${NC}"
  exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
  echo -e "${RED}Python 3.10 or higher is required. Found Python $PYTHON_VERSION${NC}"
  exit 1
fi

echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"

# Check pip
if ! command_exists pip3; then
  echo -e "${YELLOW}pip3 not found. Attempting to install...${NC}"
  
  if command_exists apt-get; then
    sudo apt-get update
    sudo apt-get install -y python3-pip
  elif command_exists dnf; then
    sudo dnf install -y python3-pip
  elif command_exists yum; then
    sudo yum install -y python3-pip
  elif command_exists pacman; then
    sudo pacman -S --noconfirm python-pip
  elif command_exists brew; then
    brew install python3
  else
    echo -e "${RED}Could not install pip3. Please install it manually.${NC}"
    exit 1
  fi
fi

# Check Git
if ! command_exists git; then
  echo -e "${YELLOW}Git not found. Attempting to install...${NC}"
  
  if command_exists apt-get; then
    sudo apt-get update
    sudo apt-get install -y git
  elif command_exists dnf; then
    sudo dnf install -y git
  elif command_exists yum; then
    sudo yum install -y git
  elif command_exists pacman; then
    sudo pacman -S --noconfirm git
  elif command_exists brew; then
    brew install git
  else
    echo -e "${RED}Could not install git. Please install it manually.${NC}"
    exit 1
  fi
fi

# Clone repository or update if already exists
INSTALL_DIR="$HOME/AutoPwnGPT"

if [ -d "$INSTALL_DIR" ]; then
  echo -e "${BLUE}Repository already exists. Updating...${NC}"
  cd "$INSTALL_DIR"
  git pull
else
  echo -e "${BLUE}Cloning repository...${NC}"
  git clone https://github.com/TonmoyInfrastructureVision/AutoPwnGPT.git "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

# Set up virtual environment
echo -e "${BLUE}Setting up virtual environment...${NC}"
if [ -d "venv" ]; then
  echo -e "${YELLOW}Virtual environment already exists. Recreate? (y/n)${NC}"
  read -p "" -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf venv
    python3 -m venv venv
  fi
else
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo -e "${BLUE}Creating necessary directories...${NC}"
mkdir -p data/logs data/reports data/sessions data/payloads

# Create default configuration
if [ ! -f "config.yaml" ]; then
  echo -e "${BLUE}Creating default configuration...${NC}"
  cp config.yaml.example config.yaml 2>/dev/null || echo -e "${YELLOW}No config example found. Using as-is.${NC}"
fi

# Setup complete
echo
echo -e "${GREEN}AutoPwnGPT has been successfully installed!${NC}"
echo
echo -e "To use AutoPwnGPT:"
echo -e "  1. Navigate to the installation directory: ${BLUE}cd $INSTALL_DIR${NC}"
echo -e "  2. Activate the virtual environment: ${BLUE}source venv/bin/activate${NC}"
echo -e "  3. Run the application: ${BLUE}python src/main.py${NC}"
echo
echo -e "For CLI-only mode: ${BLUE}python src/cli.py${NC}"
echo -e "For help: ${BLUE}python src/main.py --help${NC}"
echo
echo -e "${YELLOW}Remember to edit config.yaml to configure API keys and other settings.${NC}"
echo
echo -e "${GREEN}Happy hacking!${NC}"
