#!/bin/bash
# AutoPwnGPT Update Script

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
echo -e "${GREEN}AutoPwnGPT Update Script${NC}"
echo

# Check if we're in the AutoPwnGPT directory
if [[ ! -f "setup.py" || ! -d "src" ]]; then
  echo -e "${RED}Error: This script must be run from the AutoPwnGPT root directory.${NC}"
  exit 1
fi

# Check virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
  echo -e "${YELLOW}Virtual environment is not active. Attempting to activate...${NC}"
  
  if [[ -d "venv" ]]; then
    source venv/bin/activate
    echo -e "${GREEN}Virtual environment activated.${NC}"
  else
    echo -e "${RED}Virtual environment not found. Please run install.sh first or activate manually.${NC}"
    exit 1
  fi
fi

# Backup configuration
echo -e "${BLUE}Backing up configuration...${NC}"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
if [[ -f "config.yaml" ]]; then
  cp config.yaml "config.yaml.backup-${TIMESTAMP}"
  echo -e "${GREEN}Configuration backed up to config.yaml.backup-${TIMESTAMP}${NC}"
fi

# Pull latest changes
echo -e "${BLUE}Updating code from repository...${NC}"
# Save the current branch
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "detached")
echo -e "${BLUE}Current branch: ${CURRENT_BRANCH}${NC}"

# Stash any local changes
if ! git diff --quiet; then
  echo -e "${YELLOW}Local changes detected. Stashing changes...${NC}"
  git stash push -m "Automatic stash by update.sh on ${TIMESTAMP}"
fi

# Pull latest code
git fetch origin
git pull origin $CURRENT_BRANCH

# Apply stash if there was one
if [[ $(git stash list | grep "Automatic stash by update.sh on ${TIMESTAMP}" | wc -l) -gt 0 ]]; then
  echo -e "${BLUE}Applying stashed changes...${NC}"
  git stash pop
  
  # Check for conflicts
  if [[ $(git status -s | grep "^UU" | wc -l) -gt 0 ]]; then
    echo -e "${RED}Conflicts detected when applying your local changes.${NC}"
    echo -e "${RED}Please resolve conflicts manually and then continue with update.${NC}"
    exit 1
  fi
fi

# Update dependencies
echo -e "${BLUE}Updating dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Check for config changes
echo -e "${BLUE}Checking for configuration schema changes...${NC}"
if [[ -f "config.yaml.example" && -f "config.yaml" ]]; then
  # Use a simple diff here, could be more sophisticated with actual schema validation
  if ! diff -q "config.yaml.example" "config.yaml" &>/dev/null; then
    echo -e "${YELLOW}Configuration schema changes detected.${NC}"
    echo -e "${YELLOW}You may need to update your configuration. Please check:${NC}"
    echo -e "${YELLOW}  - New config example: config.yaml.example${NC}"
    echo -e "${YELLOW}  - Your current config: config.yaml${NC}"
    echo -e "${YELLOW}  - Your backup config: config.yaml.backup-${TIMESTAMP}${NC}"
  fi
fi

# Create new directories if needed
echo -e "${BLUE}Ensuring all required directories exist...${NC}"
mkdir -p data/logs data/reports data/sessions data/payloads

# Run database migrations if applicable
if [[ -f "src/database/migrations.py" ]]; then
  echo -e "${BLUE}Running database migrations...${NC}"
  python -c "from src.database.migrations import run_migrations; run_migrations()" || {
    echo -e "${RED}Database migration failed. You may need to run migrations manually.${NC}"
  }
fi

# Run tests to verify everything works
echo -e "${BLUE}Running tests to verify update...${NC}"
if [[ -f "scripts/test.sh" ]]; then
  bash scripts/test.sh --unit || {
    echo -e "${RED}Unit tests failed after update. Some functionality may be broken.${NC}"
    echo -e "${YELLOW}You may want to report this issue on GitHub.${NC}"
  }
fi

# Done
echo
echo -e "${GREEN}Update completed successfully!${NC}"
echo
echo -e "${BLUE}Current version:${NC}"
python -c "from src.version import __version__; print(__version__)" 2>/dev/null || echo "Version information not available"
echo
echo -e "${YELLOW}Please check for any configuration changes that may be required.${NC}"
echo
echo -e "${GREEN}To start AutoPwnGPT:${NC}"
echo -e "  GUI Mode: ${BLUE}python src/main.py${NC}"
echo -e "  CLI Mode: ${BLUE}python src/cli.py${NC}"
