#!/bin/bash

# Script to download and install E2IPlayer for Enigma2 users

# Define variables
REPO_URL="https://github.com/biko-73/E2IPlayer"
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
SETTINGS="/etc/enigma2/settings"
PLUGINPATH="/usr/lib/enigma2/python/Plugins/Extensions/"
MY_PATH="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer/"
VERSION="2025.05.09"  # Update with the appropriate version
TMP_FILE="/tmp/E2IPlayer.tar.gz"  # Path for the downloaded file
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
        REQUIRED_FOLDER="E2IPlayer_py3.9.9"
        ;;
    3.12.*)
        REQUIRED_FOLDER="E2IPlayer_py3.12x"
        ;;
    3.13.*)
        REQUIRED_FOLDER="E2IPlayer_py3.13x"
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

# Step 3: Dependency Management
echo "Checking and installing dependencies..."
#########################################
arrVar=("enigma2-plugin-extensions-e2iplayer-deps" "exteplayer3" "gstplayer" "python3-sqlite3" "python3-pycurl" "python3-json" "python3-requests" "python3-requests-cache" "python3-pycryptodome")

if [ -f /etc/opkg/opkg.conf ]; then
    Status='/var/lib/opkg/status'
    OStype='Opensource'
    Update='opkg update'
    OSinstall='opkg install'
elif [ -f /etc/apt/apt.conf ]; then
    Status='/var/lib/dpkg/status'
    OStype='DreamOS'
    Update='apt-get update'
    OSinstall='apt-get install --fix-broken --yes --assume-yes'
fi

case $(uname -m) in
    armv7l*) platform="armv7" ;;
    mips*) platform="mipsel" ;;
    sh4*) platform="sh4" ;;
    aarch64*) platform="aarch64" ;;
esac

$Update >/dev/null 2>&1

install() {
    if ! grep -qs "Package: $1" "${Status}"; then
        echo -e " >>>>   Need to install $1 <<<<"
        sleep 0.8
        echo
        ${OSinstall} "$1"
        sleep 0.8
        clear
    fi
}

for dependency in "${arrVar[@]}"; do
    install "$dependency"
done
#########################################

# Step 4: Download the repository
echo "Downloading E2IPlayer from GitHub to $TMP_FILE..."
wget -O $TMP_FILE https://codeload.github.com/biko-73/E2IPlayer/tar.gz/main

if [ $? -ne 0 ]; then
    echo "Error: Failed to download the E2IPlayer repository."
    exit 1
fi

# Step 5: Extract only the required folder
echo "Extracting only the required folder ($REQUIRED_FOLDER) to $TMP_DIR..."
mkdir -p $TMP_DIR
tar -xzf $TMP_FILE --strip-components=1 --wildcards "*/$REQUIRED_FOLDER/*" -C $TMP_DIR

if [ $? -ne 0 ]; then
    echo "Error: Failed to extract the required folder from the repository."
    exit 1
fi

# Step 6: Install E2IPlayer
echo "Installing E2IPlayer to ${INSTALL_DIR}..."
mkdir -p $INSTALL_DIR
cp -r $TMP_DIR/* $INSTALL_DIR

if [ $? -ne 0 ]; then
    echo "Error: Failed to copy files to the installation directory."
    exit 1
fi

# Step 7: Apply Settings
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
        echo "config.plugins.iptvplayer.platform=${platform}"
    } >>${SETTINGS}
fi

# Step 8: Clean up
echo "Cleaning up temporary files..."
rm -rf $TMP_FILE $TMP_DIR

# Step 9: Restart Enigma2
echo "Restarting Enigma2 to apply changes..."
init 4
sleep 5
init 3

echo "E2IPlayer installation completed!"
