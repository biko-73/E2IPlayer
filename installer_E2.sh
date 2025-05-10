#!/bin/bash

# Define variables
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
SETTINGS="/etc/enigma2/settings"
VERSION="2025.05.09"
TMP_DIR="/tmp/E2IPlayer"

# Define Python version-specific links
PYTHON_3_9_9_LINK="https://github.com/biko-73/E2IPlayer/tree/main/E2IPlayer_py3.9.9/usr/lib/enigma2/python/Plugins/Extensions"
PYTHON_3_12_LINK="https://github.com/biko-73/E2IPlayer/tree/main/E2IPlayer_py3.12x/usr/lib/enigma2/python/Plugins/Extensions"
PYTHON_3_13_LINK="https://github.com/biko-73/E2IPlayer/tree/main/E2IPlayer_py3.13x/usr/lib/enigma2/python/Plugins/Extensions"

echo "Starting the installation of E2IPlayer..."

# Step 1: Detect Python Version
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
    3.9.9)
        PLUGIN_LINK=$PYTHON_3_9_9_LINK
        ;;
    3.12.*)
        PLUGIN_LINK=$PYTHON_3_12_LINK
        ;;
    3.13.*)
        PLUGIN_LINK=$PYTHON_3_13_LINK
        ;;
    *)
        echo "> Your image's Python version: $python is not supported."
        sleep 3
        exit 1
        ;;
esac

echo "Detected supported Python version: $python"
echo "Using plugin folder: $PLUGIN_LINK"

# Step 2: Check and Remove Old Version
if [ -d "$INSTALL_DIR" ]; then
    echo "Old version of E2IPlayer detected. Removing it..."
    init 4  # Stop Enigma2
    rm -rf "$INSTALL_DIR"
    sed -i '/config.plugins.iptvplayer/d' "$SETTINGS"
    echo "Old version removed successfully."
fi

# Step 3: Download Files from the Specific Folder
echo "Downloading E2IPlayer files from the specific folder for Python $python..."
mkdir -p $TMP_DIR
mkdir -p $INSTALL_DIR

# Use `wget` to download the entire folder as a .tar.gz file
wget -q -O $TMP_DIR/E2IPlayer.tar.gz "https://github.com/biko-73/E2IPlayer/archive/refs/heads/main.tar.gz"

if [ $? -ne 0 ]; then
    echo "Error: Failed to download the E2IPlayer repository."
    exit 1
fi

# Extract only the required folder
tar -xzf $TMP_DIR/E2IPlayer.tar.gz --strip-components=7 -C $INSTALL_DIR "E2IPlayer-main/${PLUGIN_LINK##*/}"

if [ $? -ne 0 ]; then
    echo "Error: Failed to extract the required files."
    exit 1
fi

# Step 4: Apply Settings
echo "Applying settings..."
# Add your settings logic here

# Step 5: Clean up
echo "Cleaning up temporary files..."
rm -rf $TMP_DIR

# Step 6: Restart Enigma2
echo "Restarting Enigma2 to apply changes..."
init 4
sleep 5
init 3

echo "E2IPlayer installation completed!"
