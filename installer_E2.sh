#!/bin/bash

# Define variables
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
TMP_DIR="/tmp/E2IPlayer"
SETTINGS="/etc/enigma2/settings"
VERSION="2025.05.09"

# Python version-specific API links
PYTHON_3_9_9_API="https://api.github.com/repos/biko-73/E2IPlayer/contents/E2IPlayer_py3.9.9/usr/lib/enigma2/python/Plugins/Extensions"
PYTHON_3_12_API="https://api.github.com/repos/biko-73/E2IPlayer/contents/E2IPlayer_py3.12x/usr/lib/enigma2/python/Plugins/Extensions"
PYTHON_3_13_API="https://api.github.com/repos/biko-73/E2IPlayer/contents/E2IPlayer_py3.13x/usr/lib/enigma2/python/Plugins/Extensions"

echo "Starting the installation of E2IPlayer..."

# Step 1: Check Python Version
echo "Checking Python version..."
python=$(python -c "import platform; print(platform.python_version())")
pyVersion=$(python -c "import sys; print(sys.version_info[0])")
if [ "$pyVersion" != "3" ]; then
    echo "Sorry, Plugin only supports Python 3."
    exit 1
fi

case $python in
    3.9.9)
        PLUGIN_API=$PYTHON_3_9_9_API
        ;;
    3.12.*)
        PLUGIN_API=$PYTHON_3_12_API
        ;;
    3.13.*)
        PLUGIN_API=$PYTHON_3_13_API
        ;;
    *)
        echo "> Unsupported Python version: $python"
        exit 1
        ;;
esac
echo "Detected supported Python version: $python"

# Step 2: Check and Remove Old Version
if [ -d "$INSTALL_DIR" ]; then
    echo "Old version of E2IPlayer detected. Removing it..."
    init 4  # Stop Enigma2
    rm -rf "$INSTALL_DIR"
    sed -i '/config.plugins.iptvplayer/d' "$SETTINGS"
    echo "Old version removed successfully."
fi

# Step 3: Install Dependencies
echo "Checking and installing dependencies..."
if [ -f /etc/opkg/opkg.conf ]; then
    opkg update
    opkg install python3-sqlite3 python3-pycurl python3-requests
elif [ -f /etc/apt/apt.conf ]; then
    apt-get update
    apt-get install -y python3-sqlite3 python3-pycurl python3-requests
else
    echo "Error: Unsupported package manager."
    exit 1
fi

# Step 4: Download Files from GitHub API
echo "Downloading E2IPlayer files from GitHub API..."
mkdir -p $TMP_DIR
mkdir -p $INSTALL_DIR

download_files_recursively() {
    local api_url=$1
    local target_dir=$2

    curl -s "$api_url" -o "$TMP_DIR/current_folder.json"
    if [ ! -s "$TMP_DIR/current_folder.json" ]; then
        echo "Error: Failed to fetch folder contents from $api_url"
        exit 1
    fi

    cat "$TMP_DIR/current_folder.json" | jq -c '.[]' | while read -r item; do
        local type=$(echo "$item" | jq -r '.type')
        local name=$(echo "$item" | jq -r '.name')
        local download_url=$(echo "$item" | jq -r '.download_url')
        local next_url=$(echo "$item" | jq -r '.url')

        if [ "$type" = "file" ]; then
            echo "Downloading file: $name"
            wget -q -O "$target_dir/$name" "$download_url"
        elif [ "$type" = "dir" ]; then
            echo "Processing directory: $name"
            mkdir -p "$target_dir/$name"
            download_files_recursively "$next_url" "$target_dir/$name"
        fi
    done
}

download_files_recursively "$PLUGIN_API" "$INSTALL_DIR"

# Step 5: Apply Settings
echo "Applying settings..."
cat >>$SETTINGS <<EOL
config.plugins.iptvplayer.defaultMoviePlayer=exteplayer
config.plugins.iptvplayer.defaultAlternateMoviePlayer=gstplayer
config.plugins.iptvplayer.opensuborg_login=YourLogin
config.plugins.iptvplayer.opensuborg_password=YourPassword
config.plugins.iptvplayer.remember_last_position=true
config.plugins.iptvplayer.buffer_size=4096
EOL

# Step 6: Restart Enigma2
echo "Restarting Enigma2 to apply changes..."
init 4
sleep 5
init 3

# Step 7: Cleanup
echo "Cleaning up temporary files..."
rm -rf "$TMP_DIR"

echo "E2IPlayer installation completed successfully!"
