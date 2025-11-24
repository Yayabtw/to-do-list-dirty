#!/bin/bash

# Build script for to-do-list-dirty

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
pipenv run ruff check .
if [ $? -ne 0 ]; then
  echo "Error: Linter failed. Please fix the errors before building."
  exit 1
fi
echo "Linter passed!"

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
git push origin v$VERSION

echo "Creating zip archive..."
git archive --format=zip --output="todolist-v$VERSION.zip" HEAD
echo "Zip archive created: todolist-v$VERSION.zip"

