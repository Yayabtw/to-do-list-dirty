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


sed -i "s/VERSION = .*/VERSION = '$VERSION'/" tasks/settings.py

git tag -a v$VERSION -m "Release version $VERSION"
git push origin $VERSION

git archive --format=zip --output="todolist-v$VERSION.zip" HEAD

