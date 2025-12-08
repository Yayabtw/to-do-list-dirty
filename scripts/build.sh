#!/bin/bash

# Build script for to-do-list-dirty

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

# Version parameter
if [[ -z "$1" || "$1" != version=* ]]; then
  echo "Usage: $0 version=X.Y.Z"
  exit 1
fi

VERSION="${1#version=}"

if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: VERSION must follow semantic versioning (X.Y.Z)"
  exit 1
fi


echo "Building version: $VERSION"

# Run linter
echo "Running linter..."
pipenv run ruff check . --extend-ignore N802

if [ $? -ne 0 ]; then
  echo "Error: Linter failed. Please fix the errors before building."
  exit 1
fi
echo "Linter passed!"

# Run accessibility tests
echo ""
echo "Running accessibility tests..."
echo "Note: Make sure the Django server is running on http://localhost:8000/"
echo "If not, start it with: pipenv run python manage.py runserver"
echo ""
"$SCRIPT_DIR/test_accessibility.sh"
if [ $? -ne 0 ]; then
  echo "Error: Accessibility tests failed. Please fix the issues before building."
  exit 1
fi
echo "Accessibility tests passed!"

################################################################################
# Run Selenium (E2E) tests
################################################################################
echo ""
echo "Running Selenium end-to-end tests..."

SELENIUM_ERROR=0

# List of selenium test scripts to run
SELENIUM_TESTS=(
  "tests/e2e/tc016_crud_10_tasks.py"
  "tests/e2e/tc017_cross_impact.py"
)

for SELENIUM_TEST in "${SELENIUM_TESTS[@]}"; do
  if [ ! -f "$SELENIUM_TEST" ]; then
    echo "Warning: $SELENIUM_TEST not found, skipping."
    continue
  fi
  echo "Executing: $SELENIUM_TEST"
  pipenv run python "$SELENIUM_TEST"
  if [ $? -ne 0 ]; then
    echo "Error: Selenium test $SELENIUM_TEST failed. Please fix the errors before building."
    SELENIUM_ERROR=1
  fi
done

if [ $SELENIUM_ERROR -ne 0 ]; then
  echo "At least one Selenium test failed. Aborting build."
  exit 1
fi
echo "All Selenium end-to-end tests passed!"

tmpfile=$(mktemp)
awk -v ver="$VERSION" '/^VERSION = / {$0="VERSION = \x27"ver"\x27"} {print}' todo/settings.py > "$tmpfile" && mv "$tmpfile" todo/settings.py
echo "Updated version in settings.py"

# Add settings.py in commit 

echo "Adding settings.py to commit..."
git add todo/settings.py

echo "Committing changes..."
git commit -m "Bump version to $VERSION"

echo "Tagging commit..."
git tag -a v$VERSION -m "Release version $VERSION"

echo "Created tag v$VERSION"
echo "Pushing tag to remote..."
git push origin HEAD
git push origin v$VERSION

# Create releases directory if it doesn't exist
mkdir -p releases

echo "Creating zip archive..."
git archive --format=zip --output="releases/todolist-v$VERSION.zip" HEAD
echo "Zip archive created: releases/todolist-v$VERSION.zip"

