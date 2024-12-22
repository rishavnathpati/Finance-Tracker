#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Finance Tracker Installation Script${NC}"
echo "==============================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print step
print_step() {
    echo -e "\n${YELLOW}Step $1: $2${NC}"
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        python3 --version
        return 0
    elif command_exists python; then
        python --version
        return 0
    else
        return 1
    fi
}

# Function to install Python on macOS
install_python_mac() {
    echo "Installing Python using Homebrew..."
    if ! command_exists brew; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install python
}

# Function to set up virtual environment
setup_venv() {
    echo "Setting up virtual environment..."
    if [ -d "venv" ]; then
        echo "Removing existing virtual environment..."
        rm -rf venv
    fi
    python3 -m venv venv
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        echo -e "${RED}Failed to activate virtual environment${NC}"
        exit 1
    fi
}

# Main installation process
main() {
    # Step 1: Check Python installation
    print_step 1 "Checking Python installation"
    if ! check_python; then
        echo -e "${RED}Python not found!${NC}"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            install_python_mac
        else
            echo "Please install Python from https://www.python.org/downloads/"
            exit 1
        fi
    fi

    # Step 2: Set up virtual environment
    print_step 2 "Setting up virtual environment"
    setup_venv

    # Step 3: Upgrade pip
    print_step 3 "Upgrading pip"
    python3 -m pip install --upgrade pip

    # Step 4: Install Finance Tracker
    print_step 4 "Installing Finance Tracker"
    python3 -m pip install -e .

    # Step 5: Initialize application
    print_step 5 "Initializing Finance Tracker"
    python3 -m finance_tracker --init

    # Step 6: Run installation test
    print_step 6 "Running installation test"
    python3 test_installation.py

    echo -e "\n${GREEN}Installation completed successfully!${NC}"
    echo -e "\nTo start using Finance Tracker:"
    echo -e "1. Activate the virtual environment:"
    echo -e "   ${YELLOW}source venv/bin/activate${NC} (Mac/Linux)"
    echo -e "   ${YELLOW}venv\\Scripts\\activate${NC} (Windows)"
    echo -e "2. Run Finance Tracker:"
    echo -e "   ${YELLOW}finance-tracker${NC}"
    echo -e "\nFor help, see:"
    echo -e "- docs/QUICK_START.md"
    echo -e "- docs/USER_MANUAL.md"
    echo -e "- docs/TROUBLESHOOTING.md"
}

# Run main installation
main
