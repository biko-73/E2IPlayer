#!/bin/bash

# Define variables
BASE_API_URL="https://api.github.com/repos/biko-73/E2IPlayer/contents"
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
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

# Step 3: Recursive Function to Download Files
download_files_recursively() {
    local folder_url=$1
    local target_dir=$2

    # Fetch folder contents
    curl -s "$folder_url" -o $TMP_DIR/current_folder.json

    if [ $? -ne 0 ]; then
        echo "Error: Failed to fetch folder contents from $folder_url"
        exit 1
    fi

    # Parse each item in the folder
    grep '"type":' $TMP_DIR/current_folder.json | while read -r line; do
        local type=$(echo "$line" | grep -o '"type": "[^"]*' | cut -d '"' -f 4)
        local path=$(grep -o '"path": "[^"]*' $TMP_DIR/current_folder.json | cut -d '"' -f 4)
        local download_url=$(grep -o '"download_url": "[^"]*' $TMP_DIR/current_folder.json | cut -d '"' -f 4)

        if [ "$type" = "file" ]; then
            # Download the file
            echo "Downloading file: $path"
            wget -q -P "$target_dir" "$download_url"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to download $download_url"
                exit 1
            fi
        elif [ "$type" = "dir" ]; then
            # Create the directory and fetch its contents
            echo "Processing directory: $path"
            mkdir -p "$target_dir/$(basename $path)"
            download_files_recursively "$BASE_API_URL/$path?ref=main" "$target_dir/$(basename $path)"
        fi
    done
}

# Step 4: Start Recursive Download
echo "Downloading required files from GitHub API ($BASE_API_URL/$REQUIRED_FOLDER)..."
mkdir -p $TMP_DIR
mkdir -p $INSTALL_DIR

download_files_recursively "$BASE_API_URL/$REQUIRED_FOLDER?ref=main" "$INSTALL_DIR"

# Step 5: Clean up
echo "Cleaning up temporary files..."
rm -rf $TMP_DIR

# Step 6: Restart Enigma2
echo "Restarting Enigma2 to apply changes..."
init 4
sleep 5
init 3

echo "E2IPlayer installation completed!"
