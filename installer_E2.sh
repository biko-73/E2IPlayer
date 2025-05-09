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
    3.9.9)
        plugin="e2iplayer-py3.9.9"
        ;;
    3.12.*)
        plugin="e2iplayer-py3.12"
        ;;
    3.13.*)
        plugin="e2iplayer-py3.13"
        ;;
    *)
        echo "> Your image's Python version: $python is not supported."
        sleep 3
        exit 1
        ;;
esac

echo "Detected supported Python version: $python"
echo "Using plugin version: $plugin"

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

# Step 5: Extract the repository
echo "Extracting E2IPlayer to $TMP_DIR..."
mkdir -p $TMP_DIR
tar -xzf $TMP_FILE -C $TMP_DIR

if [ $? -ne 0 ]; then
    echo "Error: Failed to extract the E2IPlayer repository."
    exit 1
fi

# Step 6: Install E2IPlayer
echo "Installing E2IPlayer to ${INSTALL_DIR}..."
mkdir -p $INSTALL_DIR
cp -r $TMP_DIR/E2IPlayer-main/* $INSTALL_DIR

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
        echo "config.plugins.iptvplayer.alternative${platform^^}MoviePlayer=extgstplayer"
        echo "config.plugins.iptvplayer.alternative${platform^^}MoviePlayer0=extgstplayer"
        echo "config.plugins.iptvplayer.buforowanie_m3u8=false"
        echo "config.plugins.iptvplayer.cmdwrappath=/usr/bin/cmdwrap"
        echo "config.plugins.iptvplayer.debugprint=/tmp/iptv.dbg"
        echo "config.plugins.iptvplayer.default${platform^^}MoviePlayer=exteplayer"
        echo "config.plugins.iptvplayer.default${platform^^}MoviePlayer0=exteplayer"
        echo "config.plugins.iptvplayer.extplayer_infobanner_clockformat=24"
        echo "config.plugins.iptvplayer.extplayer_skin=line"
        echo "config.plugins.iptvplayer.extplayer_subtitle_background=transparent"
        echo "config.plugins.iptvplayer.extplayer_subtitle_border_width=1"
        echo "config.plugins.iptvplayer.extplayer_subtitle_font_size=45"
        echo "config.plugins.iptvplayer.extplayer_subtitle_line_height=65"
        echo "config.plugins.iptvplayer.f4mdumppath=/usr/bin/f4mdump"
        echo "config.plugins.iptvplayer.gstplayerpath=/usr/bin/gstplayer"
        echo "config.plugins.iptvplayer.hlsdlpath=/usr/bin/hlsdl"
        echo "config.plugins.iptvplayer.opensuborg_login=MOHAMED_OS"
        echo "config.plugins.iptvplayer.opensuborg_password=&ghost@mcee2017&"
        echo "config.plugins.iptvplayer.osk_type=system"
        echo "config.plugins.iptvplayer.platform=${platform}"
        echo "config.plugins.iptvplayer.remember_last_position=true"
        echo "config.plugins.iptvplayer.rtmpdumppath=/usr/bin/rtmpdump"
        echo "config.plugins.iptvplayer.uchardetpath=/usr/bin/uchardet"
        echo "config.plugins.iptvplayer.updateLastCheckedVersion=${VERSION}"
        echo "config.plugins.iptvplayer.usepycurl=True"
        echo "config.plugins.iptvplayer.watched_item_color=#FF0000"
        echo "config.plugins.iptvplayer.wgetpath=wget"
        echo "config.plugins.iptvplayer.ytDefaultformat=9999"
        echo "config.plugins.iptvplayer.ytUseDF=False"
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
