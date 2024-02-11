#!/bin/bash

set -e  # Exit on error



# Confirm Docker/Podman availability
if ! command -v "docker" >/dev/null 2>&1 && ! command -v "podman" >/dev/null 2>&1; then
  echo "Error: Neither Docker nor Podman found. Please install one of them."
  exit 1
fi


# Build docker image (corrected Dockerfile path and quoting)
RUNNER=$(command -v podman || command -v docker)  # Use whichever is available
$RUNNER build \
    -f "Dockerfile" \
    -t "nobinkhan/ad_scrapper" .

echo "Docker image built successfully."

$RUNNER run \
  --rm \
  --name ad_scrapper \
  -p 8000:80 \
  nobinkhan/ad_scrapper
