#!/bin/bash

# Script to download and install E2IPlayer for Enigma2 users

# Define variables
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
SETTINGS="/etc/enigma2/settings"
PLUGINPATH="/usr/lib/enigma2/python/Plugins/Extensions/"

BASE_URL="https://github.com/biko-73/E2IPlayer/tree/main"
PY3_9_9_FOLDER="$BASE_URL/E2IPlayer_py3.9.9/usr/lib/enigma2/python/Plugins/Extensions"
PY3_12X_FOLDER="$BASE_URL/E2IPlayer_py3.12x/usr/lib/enigma2/python/Plugins/Extensions"
PY3_13X_FOLDER="$BASE_URL/E2IPlayer_py3.13x/usr/lib/enigma2/python/Plugins/Extensions"

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
        DOWNLOAD_URL="$PY3_9_9_FOLDER"
        ;;
    3.12.*)
        DOWNLOAD_URL="$PY3_12X_FOLDER"
        ;;
    3.13.*)
        DOWNLOAD_URL="$PY3_13X_FOLDER"
        ;;
    *)
        echo "> Your image's Python version: $python is not supported."
        sleep 3
        exit 1
        ;;
esac

echo "Detected supported Python version: $python"
echo "Using folder: $DOWNLOAD_URL"

# Step 2: Check and Remove Old Version
if [ -d "$INSTALL_DIR" ]; then
    echo "Old version of E2IPlayer detected. Removing it..."
    init 4  # Stop Enigma2
    rm -rf "$INSTALL_DIR"
    sed -i '/config.plugins.iptvplayer/d' "$SETTINGS"
    echo "Old version removed successfully."
fi

# Step 3: Download only the required folder
echo "Downloading only the required folder ($DOWNLOAD_URL)..."
mkdir -p $TMP_DIR
cd $TMP_DIR

# Clone the folder contents
wget -r -np -nH --cut-dirs=6 -R "index.html*" "$DOWNLOAD_URL"

if [ $? -ne 0 ]; then
    echo "Error: Failed to download the required folder."
    exit 1
fi

# Step 4: Install E2IPlayer
echo "Installing E2IPlayer to ${INSTALL_DIR}..."
mkdir -p $INSTALL_DIR
cp -r $TMP_DIR/* $INSTALL_DIR

if [ $? -ne 0 ]; then
    echo "Error: Failed to copy files to the installation directory."
    exit 1
fi

# Step 5: Apply Settings
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

# Step 6: Clean up
echo "Cleaning up temporary files..."
rm -rf $TMP_DIR

# Step 7: Restart Enigma2
echo "Restarting Enigma2 to apply changes..."
init 4
sleep 5
init 3

echo "E2IPlayer installation completed!"
