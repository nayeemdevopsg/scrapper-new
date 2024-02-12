#!/bin/bash

set -e  # Exit on error

# Confirm Docker/Podman availability
if ! command -v "docker" >/dev/null 2>&1 && ! command -v "podman" >/dev/null 2>&1; then
  echo "Error: Neither Docker nor Podman found. Please install one of them."
  exit 1
fi

# Get architecture (32-bit or 64-bit)
arch=$(uname -m)

# Define base URL for different distributions
base_url="https://dl.google.com/linux/direct/"

# Define package names based on architecture
case $arch in
  "i686" | "x86_64")
    package_name="google-chrome-stable_current_${arch}.rpm"
    ;;
  *)
    echo "Unsupported architecture: $arch"
    exit 1
    ;;
esac

# Check if package already exists
download_path="./$package_name"  # Customize download path if needed

if [[ -f "$download_path" ]]; then
  echo "Google Chrome RPM already exists: $download_path"
  echo "Skipping download."
else
  # Download URL
  download_url="${base_url}${package_name}"

  # Download the package
  wget "${download_url}"

  # Check if download was successful
  if [[ $? -ne 0 ]]; then
    echo "Failed to download package: $package_name"
    exit 1
  fi

  echo "Downloaded Google Chrome RPM successfully!"

fi

HOST_UID=$(id -u) 
HOST_GID=$(id -g)

# Gather project files
rm -rf temp_copy
rsync -rav ./ temp_copy/ \
    --exclude=".git" \
    --exclude=".gitignore" \
    --exclude=".gitlab-ci.yml" \
    --exclude=".vscode" \
    --exclude="Pipfile" \
    --exclude="poetry.lock" \
    --exclude="pyproject.toml" \
    --exclude="appspec.yml" \
    --exclude="backup.sqlite3" \
    --exclude="buildspec.yml" \
    --exclude="google-chrome-stable_current_x86_64.rpm" \
    --exclude="readme.MD" \
    --exclude="docker_run.sh" \
    --exclude="ads.csv" \
    --exclude="keywords.csv" \
    --exclude=".Dockerignore" \
    --exclude="Dockerfile" \
    --exclude="Dockerfile-Backup" \
    --exclude="docker-compose.yml" \
    --exclude="docker-entrypoint.sh" \
    --exclude="docker/" \
    --exclude="temp_copy/" \
    --exclude="venv/" \
    --exclude="__pycache__"

# Files copy ends


# Build docker image (corrected Dockerfile path and quoting)
RUNNER=$(command -v podman || command -v docker)  # Use whichever is available
$RUNNER build --build-arg UID=$HOST_UID --build-arg GID=$HOST_GID \
    -f "Dockerfile" \
    -t "nobinkhan/ad_scrapper" .

echo "Docker image built successfully."
rm -rf temp_copy
$RUNNER run \
  --rm \
  --name ad_scrapper \
  -p 8000:8000 \
  nobinkhan/ad_scrapper
