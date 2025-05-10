#!/bin/bash

# Define variables
BASE_API_URL="https://api.github.com/repos/biko-73/E2IPlayer/contents"
INSTALL_DIR="/usr/lib/enigma2/python/Plugins/Extensions/E2IPlayer"
TMP_DIR="/tmp/E2IPlayer"

echo "Starting the installation of E2IPlayer..."

# Recursive Function to Download Files
download_files_recursively() {
    local folder_url=$1
    local target_dir=$2

    # Fetch folder contents
    for attempt in {1..3}; do
        curl -s "$folder_url" -o $TMP_DIR/current_folder.json && break
        echo "Retrying folder fetch ($attempt/3): $folder_url"
        sleep 2
    done

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
            local encoded_download_url=$(echo "$download_url" | sed 's/ /%20/g')
            echo "Downloading file: $path"

            for attempt in {1..3}; do
                wget -q -P "$target_dir" "$encoded_download_url" && break
                echo "Retrying file download ($attempt/3): $encoded_download_url"
                sleep 2
            done

            if [ $? -ne 0 ]; then
                echo "Error: Failed to download $encoded_download_url after 3 attempts"
                exit 1
            fi
        elif [ "$type" = "dir" ]; then
            local dir_name=$(echo "$path" | awk -F '/' '{print $NF}')
            echo "Processing directory: $dir_name"
            mkdir -p "$target_dir/$dir_name"
            download_files_recursively "$BASE_API_URL/$path?ref=main" "$target_dir/$dir_name"
        fi
    done
}

# Start Recursive Download
echo "Downloading required files from GitHub API ($BASE_API_URL)..."
mkdir -p $TMP_DIR
mkdir -p $INSTALL_DIR

download_files_recursively "$BASE_API_URL?ref=main" "$INSTALL_DIR"

# Clean up
echo "Cleaning up temporary files..."
rm -rf $TMP_DIR

# Restart Enigma2
echo "Restarting Enigma2 to apply changes..."
init 4
sleep 5
init 3

echo "E2IPlayer installation completed!"
