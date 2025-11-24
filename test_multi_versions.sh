#!/bin/bash

# Script to test the application with multiple Python and Django versions
# Usage: ./test_multi_versions.sh

set -e

echo "=== Multi-Version Testing Script ==="
echo ""

# Note: Python 2.7 is no longer supported by Django (last supported version was Django 1.11)
# We will test with Python 3.9 and 3.13, and Django 3.x, 4.x, 5.x

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test with a specific Python and Django version
test_version() {
    local python_version=$1
    local django_version=$2
    
    echo -e "${YELLOW}Testing with Python ${python_version} and Django ${django_version}${NC}"
    
    # Check if Python version is available
    if ! command -v python${python_version} &> /dev/null; then
        echo -e "${RED}Python ${python_version} not found, skipping...${NC}"
        echo ""
        return
    fi
    
    # Create a temporary virtual environment
    temp_venv=$(mktemp -d)
    python${python_version} -m venv "$temp_venv"
    source "$temp_venv/bin/activate"
    
    # Install Django and dependencies
    pip install -q Django${django_version} coverage
    
    # Run tests
    if coverage run --source='.' manage.py test tasks.tests > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Tests passed with Python ${python_version} and Django ${django_version}${NC}"
    else
        echo -e "${RED}✗ Tests failed with Python ${python_version} and Django ${django_version}${NC}"
    fi
    
    # Cleanup
    deactivate
    rm -rf "$temp_venv"
    echo ""
}

# Test matrix
# Python 3.9 with Django 3.2 and 4.2
test_version "3.9" ">=3.2,<3.3"
test_version "3.9" ">=4.2,<4.3"

# Python 3.13 with Django 4.2 and 5.0
test_version "3.13" ">=4.2,<4.3"
test_version "3.13" ">=5.0,<5.1"

echo -e "${GREEN}=== Multi-Version Testing Complete ===${NC}"
