#!/bin/bash

# Define variables
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
TMP_DIR="/tmp/E2IPlayer"

# Define Python version-specific API links
PYTHON_3_9_9_API="https://api.github.com/repos/biko-73/E2IPlayer/contents/E2IPlayer_py3.9.9/usr/lib/enigma2/python/Plugins/Extensions"
PYTHON_3_12_API="https://api.github.com/repos/biko-73/E2IPlayer/contents/E2IPlayer_py3.12x/usr/lib/enigma2/python/Plugins/Extensions"
PYTHON_3_13_API="https://api.github.com/repos/biko-73/E2IPlayer/contents/E2IPlayer_py3.13x/usr/lib/enigma2/python/Plugins/Extensions"

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
        PLUGIN_API=$PYTHON_3_9_9_API
        ;;
    3.12.*)
        PLUGIN_API=$PYTHON_3_12_API
        ;;
    3.13.*)
        PLUGIN_API=$PYTHON_3_13_API
        ;;
    *)
        echo "> Your image's Python version: $python is not supported."
        sleep 3
        exit 1
        ;;
esac

echo "Detected supported Python version: $python"
echo "Using plugin API: $PLUGIN_API"

# Step 2: Clean Up Old Installation
if [ -d "$INSTALL_DIR" ]; then
    echo "Old version of E2IPlayer detected. Removing it..."
    init 4  # Stop Enigma2
    rm -rf "$INSTALL_DIR"
    echo "Old version removed successfully."
fi

# Step 3: Download Files from GitHub API
echo "Downloading E2IPlayer files from GitHub API..."
mkdir -p $TMP_DIR
mkdir -p $INSTALL_DIR

download_files_recursively() {
    local api_url=$1
    local target_dir=$2

    # Fetch folder contents
    curl -s "$api_url" -o $TMP_DIR/current_folder.json

    if [ ! -s $TMP_DIR/current_folder.json ]; then
        echo "Error: Failed to fetch folder contents from $api_url"
        exit 1
    fi

    # Parse each item in the folder
    grep '"type":' $TMP_DIR/current_folder.json | while read -r line; do
        local type=$(echo "$line" | grep -o '"type": "[^"]*' | cut -d '"' -f 4)
        local path=$(grep -o '"path": "[^"]*' $TMP_DIR/current_folder.json | cut -d '"' -f 4)
        local download_url=$(grep -o '"download_url": "[^"]*' $TMP_DIR/current_folder.json | cut -d '"' -f 4)

        if [ "$type" = "file" ]; then
            echo "Downloading file: $path"
            wget -q -P "$target_dir" "$download_url"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to download $download_url"
                exit 1
            fi
        elif [ "$type" = "dir" ]; then
            local dir_name=$(basename "$path")
            echo "Processing directory: $dir_name"
            mkdir -p "$target_dir/$dir_name"
            download_files_recursively "${api_url}/${dir_name}" "$target_dir/$dir_name"
        fi
    done
}

download_files_recursively "$PLUGIN_API" "$INSTALL_DIR"

# Step 4: Restart Enigma2
echo "Restarting Enigma2 to apply changes..."
init 4
sleep 5
init 3

echo "E2IPlayer installation completed!"
