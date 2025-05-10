#!/bin/bash

# Script to download and install E2IPlayer for Enigma2 users

# Define variables
BASE_API_URL="https://api.github.com/repos/biko-73/E2IPlayer/contents"
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
SETTINGS="/etc/enigma2/settings"
PLUGINPATH="/usr/lib/enigma2/python/Plugins/Extensions/"
MY_PATH="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer/"
VERSION="2025.05.09"
TMP_DIR="/tmp/E2IPlayer"

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
        plugin_folder="E2IPlayer_py3.9.9"
        ;;
    3.12.*)
        plugin_folder="E2IPlayer_py3.12x"
        ;;
    3.13.*)
        plugin_folder="E2IPlayer_py3.13x"
        ;;
    *)
        echo "> Your image's Python version: $python is not supported."
        sleep 3
        exit 1
        ;;
esac

echo "Detected supported Python version: $python"
echo "Using plugin folder: $plugin_folder"

# Step 2: Check and Remove Old Version
if [ -d "$INSTALL_DIR" ]; then
    echo "Old version of E2IPlayer detected. Removing it..."
    init 4  # Stop Enigma2
    rm -rf "$INSTALL_DIR"
    sed -i '/config.plugins.iptvplayer/d' "$SETTINGS"
    echo "Old version removed successfully."
fi

# Step 3: Download Specific Folder
echo "Downloading E2IPlayer files for Python $python from GitHub..."

mkdir -p $TMP_DIR
mkdir -p $INSTALL_DIR

download_files_recursively() {
    local folder_url=$1
    local target_dir=$2

    # Fetch folder contents
    curl -s "$folder_url" -o $TMP_DIR/current_folder.json

    if [ ! -s $TMP_DIR/current_folder.json ]; then
        echo "Error: Failed to fetch folder contents from $folder_url"
        exit 1
    fi

    # Parse each item in the folder
    grep '"type":' $TMP_DIR/current_folder.json | while read -r line; do
        local type=$(echo "$line" | grep -o '"type": "[^"]*' | cut -d '"' -f 4)
        local path=$(grep -o '"path": "[^"]*' $TMP_DIR/current_folder.json | cut -d '"' -f 4)
        local download_url=$(grep -o '"download_url": "[^"]*' $TMP_DIR/current_folder.json | cut -d '"' -f 4)

        if [ "$type" = "file" ]; then
            # Encode spaces in URLs
            local encoded_download_url=$(echo "$download_url" | sed 's/ /%20/g')
            echo "Downloading file: $path"
            wget -q -P "$target_dir" "$encoded_download_url"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to download $encoded_download_url"
                exit 1
            fi
        elif [ "$type" = "dir" ]; then
            local dir_name=$(echo "$path" | awk -F '/' '{print $NF}')
            echo "Processing directory: $dir_name"
            mkdir -p "$target_dir/$dir_name"
            download_files_recursively "${BASE_API_URL}/$path?ref=main" "$target_dir/$dir_name"
        fi
    done
}

download_files_recursively "$BASE_API_URL/$plugin_folder?ref=main" "$INSTALL_DIR"

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
        echo "config.plugins.iptvplayer.platform=${platform}"
        echo "config.plugins.iptvplayer.updateLastCheckedVersion=${VERSION}"
        # Add more settings as needed
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
