#!/bin/bash

# Script to download and install E2IPlayer for Enigma2 users

# Define variables
GIT_REPO="https://github.com/biko-73/E2IPlayer.git"
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
SETTINGS="/etc/enigma2/settings"
PLUGINPATH="/usr/lib/enigma2/python/Plugins/Extensions/"

TMP_DIR="/tmp/E2IPlayer"  # Temporary directory for extraction

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
    sed -i '/config.plugins.iptvplayer/d' "$SETTINGS"
    echo "Old version removed successfully."
fi

# Step 3: Clone the repository and copy the required folder
echo "Cloning the repository and extracting the required folder..."
mkdir -p $TMP_DIR
git clone --depth 1 "$GIT_REPO" $TMP_DIR

if [ $? -ne 0 ]; then
    echo "Error: Failed to clone the repository."
    exit 1
fi

# Copy only the required folder
mkdir -p $INSTALL_DIR
cp -r $TMP_DIR/$REQUIRED_FOLDER/* $INSTALL_DIR

if [ $? -ne 0 ]; then
    echo "Error: Failed to copy files to the installation directory."
    exit 1
fi

# Step 4: Apply Settings
echo "Applying settings..."
sleep 3
if [ -e "${PLUGINPATH}IPTVPlayer" ]; then
    echo "> Applying settings..."
    sleep 3
    echo "> Your device will restart now, please wait..."
    init 4
    sleep 5
    sed -e s/config.plugins.iptvplayer.*//g -i ${SETTINGS}
    sleep 2
    {
        echo "config.plugins.iptvplayer.AktualizacjaWmenu=true"
        echo "config.plugins.iptvplayer.buforowanie_m3u8=false"
        echo "config.plugins.iptvplayer.usepycurl=True"
    } >>${SETTINGS}
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
