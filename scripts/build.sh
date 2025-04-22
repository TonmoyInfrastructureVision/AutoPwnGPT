#!/bin/bash
# AutoPwnGPT Build Script

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
echo -e "${GREEN}AutoPwnGPT Build Script${NC}"
echo

# Parse arguments
BUILD_TYPE="package"
BUILD_DOCKER=false
BUILD_INSTALLER=false
BUILD_DOCS=false
CLEAN=false
RELEASE=false
VERSION=""

for arg in "$@"; do
  case $arg in
    --docker)
      BUILD_DOCKER=true
      shift
      ;;
    --installer)
      BUILD_INSTALLER=true
      shift
      ;;
    --docs)
      BUILD_DOCS=true
      shift
      ;;
    --clean)
      CLEAN=true
      shift
      ;;
    --release)
      RELEASE=true
      shift
      ;;
    --version=*)
      VERSION="${arg#*=}"
      shift
      ;;
    --help|-h)
      echo -e "Usage: $0 [OPTIONS]"
      echo -e "Options:"
      echo -e "  --docker       Build Docker image"
      echo -e "  --installer    Build installer package"
      echo -e "  --docs         Build documentation"
      echo -e "  --clean        Clean build artifacts before building"
      echo -e "  --release      Prepare a release build"
      echo -e "  --version=X.Y.Z Set the version for the build"
      echo -e "  --help, -h     Show this help message"
      exit 0
      ;;
  esac
done

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
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    source venv/bin/activate
  fi
fi

# Install build dependencies
echo -e "${BLUE}Installing build dependencies...${NC}"
pip install --upgrade pip wheel build setuptools twine

# Clean if requested
if [[ "$CLEAN" == true ]]; then
  echo -e "${BLUE}Cleaning build artifacts...${NC}"
  rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .coverage htmlcov/
  find . -type d -name "__pycache__" -exec rm -rf {} +
  find . -type d -name "*.egg-info" -exec rm -rf {} +
  find . -type f -name "*.pyc" -delete
  find . -type f -name "*.pyo" -delete
  find . -type f -name "*.pyd" -delete
  find . -type f -name ".coverage" -delete
  find . -type d -name "htmlcov" -exec rm -rf {} +
  find . -type d -name ".pytest_cache" -exec rm -rf {} +
  echo -e "${GREEN}Build artifacts cleaned.${NC}"
fi

# Update version if specified
if [[ -n "$VERSION" ]]; then
  echo -e "${BLUE}Setting version to ${VERSION}...${NC}"
  # Update version in version.py
  if [[ -f "src/version.py" ]]; then
    echo "__version__ = \"$VERSION\"" > src/version.py
    echo -e "${GREEN}Version updated in src/version.py${NC}"
  fi
  
  # Also update setup.py if it exists
  if [[ -f "setup.py" ]]; then
    sed -i "s/version=.*,/version=\"$VERSION\",/" setup.py
    echo -e "${GREEN}Version updated in setup.py${NC}"
  fi
fi

# Run tests before building
echo -e "${BLUE}Running tests...${NC}"
pip install -r requirements-dev.txt

# Run tests, but allow continuation even if they fail in non-release mode
if [[ "$RELEASE" == true ]]; then
  pytest || {
    echo -e "${RED}Tests failed. Cannot create release build!${NC}"
    exit 1
  }
else
  pytest || echo -e "${YELLOW}Tests failed, but continuing with build as this is not a release build.${NC}"
fi

# Build Python package
echo -e "${BLUE}Building Python package...${NC}"
python -m build

# Check if the build was successful
if [[ ! -d "dist" ]]; then
  echo -e "${RED}Build failed: dist directory not created.${NC}"
  exit 1
fi

echo -e "${GREEN}Python package built successfully.${NC}"
echo -e "${BLUE}Build artifacts:${NC}"
ls -la dist/

# Build Docker image if requested
if [[ "$BUILD_DOCKER" == true ]]; then
  echo -e "${BLUE}Building Docker image...${NC}"
  
  # Get version for tagging
  if [[ -z "$VERSION" && -f "src/version.py" ]]; then
    VERSION=$(python -c "import sys; sys.path.insert(0, '.'); from src.version import __version__; print(__version__)")
  fi
  
  # Use version or latest tag
  DOCKER_TAG=${VERSION:-latest}
  
  # Build the Docker image
  docker build -t "autopwngpt:$DOCKER_TAG" .
  
  echo -e "${GREEN}Docker image built: autopwngpt:$DOCKER_TAG${NC}"
  
  # Save the Docker image to a file if it's a release
  if [[ "$RELEASE" == true ]]; then
    echo -e "${BLUE}Saving Docker image to file...${NC}"
    docker save "autopwngpt:$DOCKER_TAG" | gzip > "dist/autopwngpt-docker-$DOCKER_TAG.tar.gz"
    echo -e "${GREEN}Docker image saved to dist/autopwngpt-docker-$DOCKER_TAG.tar.gz${NC}"
  fi
fi

# Build installer if requested
if [[ "$BUILD_INSTALLER" == true ]]; then
  echo -e "${BLUE}Building installer package...${NC}"
  
  # Create a unified installer script that includes all necessary scripts
  echo -e "${BLUE}Creating installer package...${NC}"
  
  # Determine the version
  if [[ -z "$VERSION" && -f "src/version.py" ]]; then
    VERSION=$(python -c "import sys; sys.path.insert(0, '.'); from src.version import __version__; print(__version__)")
  fi
  VERSION=${VERSION:-"dev"}
  
  # Create a compressed tarball
  mkdir -p dist/installer
  cp -r src scripts requirements.txt config.yaml setup.py README.md LICENSE dist/installer/
  
  # Create a self-extracting installer
  cat << 'EOF' > dist/installer/install_autopwngpt.sh
#!/bin/bash
set -e

echo "AutoPwnGPT Installer"
echo "This will install AutoPwnGPT on your system."

# Check for Python 3.10+
if ! command -v python3 &> /dev/null; then
  echo "Python 3 is required but not found. Please install Python 3.10 or higher."
  exit 1
fi

# Create installation directory
INSTALL_DIR="${HOME}/.autopwngpt"
mkdir -p "$INSTALL_DIR"

# Extract files to installation directory
echo "Extracting files to $INSTALL_DIR..."
cp -r * "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create symlink to executable
mkdir -p "${HOME}/.local/bin"
cat << 'EXEOF' > "${HOME}/.local/bin/autopwngpt"
#!/bin/bash
# AutoPwnGPT launcher
cd "${HOME}/.autopwngpt"
source venv/bin/activate
python src/main.py "$@"
EXEOF
chmod +x "${HOME}/.local/bin/autopwngpt"

echo "Installation complete!"
echo "You can now run AutoPwnGPT using the 'autopwngpt' command."
echo "Make sure ${HOME}/.local/bin is in your PATH."
EOF
  
  chmod +x dist/installer/install_autopwngpt.sh
  
  # Create tarball
  cd dist
  tar czf "autopwngpt-installer-$VERSION.tar.gz" installer/
  rm -rf installer/
  cd ..
  
  echo -e "${GREEN}Installer package created: dist/autopwngpt-installer-$VERSION.tar.gz${NC}"
fi

# Build documentation if requested
if [[ "$BUILD_DOCS" == true ]]; then
  echo -e "${BLUE}Building documentation...${NC}"
  
  # Check if mkdocs is installed
  if ! command -v mkdocs &> /dev/null; then
    echo -e "${YELLOW}mkdocs not found. Installing...${NC}"
    pip install mkdocs mkdocs-material
  fi
  
  # Build docs
  mkdocs build
  
  # Check if the build was successful
  if [[ ! -d "site" ]]; then
    echo -e "${RED}Documentation build failed: site directory not created.${NC}"
  else
    echo -e "${GREEN}Documentation built successfully. Output in 'site' directory${NC}"
    
    # Package docs if this is a release
    if [[ "$RELEASE" == true ]]; then
      echo -e "${BLUE}Packaging documentation...${NC}"
      cd site
      zip -r "../dist/autopwngpt-docs-${VERSION:-dev}.zip" .
      cd ..
      echo -e "${GREEN}Documentation packaged: dist/autopwngpt-docs-${VERSION:-dev}.zip${NC}"
    fi
  fi
fi

# Prepare release if requested
if [[ "$RELEASE" == true ]]; then
  echo -e "${BLUE}Preparing release...${NC}"
  
  # Ensure we have a version
  if [[ -z "$VERSION" ]]; then
    echo -e "${RED}Cannot prepare release without a version. Use --version=X.Y.Z${NC}"
    exit 1
  fi
  
  # Create release notes template if not exists
  if [[ ! -f "RELEASE_NOTES.md" ]]; then
    cat << EOF > RELEASE_NOTES.md
# Release Notes for AutoPwnGPT $VERSION

## New Features
- 

## Bug Fixes
- 

## Improvements
- 

## Breaking Changes
- 

## Security Updates
- 
EOF
    echo -e "${YELLOW}Created RELEASE_NOTES.md template. Please fill in the details.${NC}"
    echo -e "${YELLOW}After filling in the release notes, run this script again with the same options.${NC}"
    exit 0
  fi
  
  # Create GitHub release artifact
  echo -e "${BLUE}Creating GitHub release artifact...${NC}"
  cp RELEASE_NOTES.md dist/
  cd dist
  zip "autopwngpt-$VERSION-release.zip" *.whl *.tar.gz RELEASE_NOTES.md
  cd ..
  
  echo -e "${GREEN}GitHub release artifact created: dist/autopwngpt-$VERSION-release.zip${NC}"
  echo -e "${YELLOW}Upload this file to the GitHub release page.${NC}"
  
  # Instructions for publishing to PyPI
  echo -e "${BLUE}To publish to PyPI, run:${NC}"
  echo -e "${GREEN}python -m twine upload dist/*.whl dist/*.tar.gz${NC}"
fi

# Done
echo -e "\n${GREEN}Build process completed successfully!${NC}"
