#!/bin/bash

# Script to download and install E2IPlayer for Enigma2 users

# Define variables
BASE_API_URL="https://api.github.com/repos/biko-73/E2IPlayer/contents"
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
TMP_DIR="/tmp/E2IPlayer"
ACCESS_TOKEN="your_github_personal_access_token" # Optional, if rate limits are an issue

echo "Starting the installation of E2IPlayer..."

# Step 1: Check Python version
echo "Checking Python version..."
python=$(python -c "import platform; print(platform.python_version())")
pyVersion=$(python -c "import sys; print(sys.version_info[0])")
sleep 1
if [ "$pyVersion" != "3" ]; then
    echo "Sorry, Plugin does not support Python 2."
    sleep 4
    exit 1
fi

case $python in
    3.9.*)
        REQUIRED_FOLDER="E2IPlayer_py3.9.9/usr/lib/enigma2/python/Plugins/Extensions"
        ;;
    3.12.*)
        REQUIRED_FOLDER="E2IPlayer_py3.12x/usr/lib/enigma2/python/Plugins/Extensions"
        ;;
    3.13.*)
        REQUIRED_FOLDER="E2IPlayer_py3.13x/usr/lib/enigma2/python/Plugins/Extensions"
        ;;
    *)
        echo "> Your image's Python version: $python is not supported."
        sleep 3
        exit 1
        ;;
esac

echo "Detected supported Python version: $python"
echo "Using folder: $REQUIRED_FOLDER"

# Step 2: Check and Remove Old Version
if [ -d "$INSTALL_DIR" ]; then
    echo "Old version of E2IPlayer detected. Removing it..."
    init 4  # Stop Enigma2
    rm -rf "$INSTALL_DIR"
    echo "Old version removed successfully."
fi

# Step 3: Fetch the Required Folder Using GitHub API
echo "Downloading required files from GitHub API ($BASE_API_URL/$REQUIRED_FOLDER)..."
mkdir -p $TMP_DIR

# Fetch file list from the folder
if [ -z "$ACCESS_TOKEN" ]; then
    curl -s "$BASE_API_URL/$REQUIRED_FOLDER" -o $TMP_DIR/file_list.json
else
    curl -s -H "Authorization: token $ACCESS_TOKEN" "$BASE_API_URL/$REQUIRED_FOLDER" -o $TMP_DIR/file_list.json
fi

if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch file list from $BASE_API_URL/$REQUIRED_FOLDER"
    exit 1
fi

# Download each file from the folder
for file_url in $(jq -r '.[].download_url' $TMP_DIR/file_list.json); do
    wget -q -P $TMP_DIR "$file_url"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download $file_url"
        exit 1
    fi
done

# Step 4: Install E2IPlayer
echo "Installing E2IPlayer to $INSTALL_DIR..."
mkdir -p $INSTALL_DIR
cp -r $TMP_DIR/* $INSTALL_DIR

if [ $? -ne 0 ]; then
    echo "Error: Failed to copy files to the installation directory."
    exit 1
fi

# Step 5: Clean up
echo "Cleaning up temporary files..."
rm -rf $TMP_DIR

# Step 6: Restart Enigma2
echo "Restarting Enigma2 to apply changes..."
init 4
sleep 5
init 3

echo "E2IPlayer installation completed!"
