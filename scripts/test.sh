#!/bin/bash
# AutoPwnGPT Test Script

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
echo -e "${GREEN}AutoPwnGPT Test Runner${NC}"
echo

# Check if virtual environment is active
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

# Check for pytest
if ! python -c "import pytest" &> /dev/null; then
  echo -e "${YELLOW}pytest not found. Installing...${NC}"
  pip install pytest pytest-cov pytest-xdist
fi

# Parse arguments
RUN_ALL=true
RUN_UNIT=false
RUN_INTEGRATION=false
RUN_FUNCTIONAL=false
COVERAGE=false
VERBOSE=false
PARALLEL=false

for arg in "$@"; do
  case $arg in
    --unit)
      RUN_ALL=false
      RUN_UNIT=true
      shift
      ;;
    --integration)
      RUN_ALL=false
      RUN_INTEGRATION=true
      shift
      ;;
    --functional)
      RUN_ALL=false
      RUN_FUNCTIONAL=true
      shift
      ;;
    --coverage)
      COVERAGE=true
      shift
      ;;
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --parallel|-p)
      PARALLEL=true
      shift
      ;;
    --help|-h)
      echo -e "Usage: $0 [OPTIONS]"
      echo -e "Options:"
      echo -e "  --unit         Run unit tests only"
      echo -e "  --integration  Run integration tests only"
      echo -e "  --functional   Run functional tests only"
      echo -e "  --coverage     Generate coverage report"
      echo -e "  --verbose, -v  Run tests with verbose output"
      echo -e "  --parallel, -p Run tests in parallel"
      echo -e "  --help, -h     Show this help message"
      exit 0
      ;;
  esac
done

# Build test command
TEST_CMD="python -m pytest"

if [[ "$VERBOSE" == true ]]; then
  TEST_CMD+=" -v"
fi

if [[ "$PARALLEL" == true ]]; then
  TEST_CMD+=" -xvs"
fi

if [[ "$COVERAGE" == true ]]; then
  TEST_CMD+=" --cov=src --cov-report=term --cov-report=html:coverage"
fi

# Run tests
echo -e "${BLUE}Running tests...${NC}"

if [[ "$RUN_ALL" == true ]]; then
  echo -e "${BLUE}Running all tests${NC}"
  $TEST_CMD tests/
  
  TEST_STATUS=$?
else
  TEST_PATHS=""
  
  if [[ "$RUN_UNIT" == true ]]; then
    echo -e "${BLUE}Running unit tests${NC}"
    TEST_PATHS+=" tests/unit/"
  fi
  
  if [[ "$RUN_INTEGRATION" == true ]]; then
    echo -e "${BLUE}Running integration tests${NC}"
    TEST_PATHS+=" tests/integration/"
  fi
  
  if [[ "$RUN_FUNCTIONAL" == true ]]; then
    echo -e "${BLUE}Running functional tests${NC}"
    TEST_PATHS+=" tests/functional/"
  fi
  
  $TEST_CMD $TEST_PATHS
  
  TEST_STATUS=$?
fi

# Print results
if [[ $TEST_STATUS -eq 0 ]]; then
  echo -e "${GREEN}All tests passed!${NC}"
  
  if [[ "$COVERAGE" == true ]]; then
    echo -e "${BLUE}Coverage report generated in 'coverage' directory.${NC}"
    echo -e "${BLUE}Open coverage/index.html in your browser to view detailed coverage report.${NC}"
  fi
else
  echo -e "${RED}Tests failed with status code $TEST_STATUS.${NC}"
  exit $TEST_STATUS
fi

# Run linting
echo -e "\n${BLUE}Running linting checks...${NC}"

if ! python -c "import flake8" &> /dev/null; then
  echo -e "${YELLOW}flake8 not found. Installing...${NC}"
  pip install flake8
fi

flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics

LINT_STATUS=$?

if [[ $LINT_STATUS -eq 0 ]]; then
  echo -e "${GREEN}Linting checks passed!${NC}"
else
  echo -e "${RED}Linting checks failed.${NC}"
  exit $LINT_STATUS
fi

echo -e "\n${GREEN}All tests and checks completed successfully!${NC}"
