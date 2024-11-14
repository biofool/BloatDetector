#!/bin/bash

# Source and destination paths
SRC_SCRIPT_PATH="./CollectFileUsageStats.sh"
DEST_DIR=${1:-/usr/local/bin}

# Prepare destination script path
DEST_SCRIPT_PATH="$DEST_DIR/$(basename $SRC_SCRIPT_PATH)"

# Copy the script to the destination directory
sudo cp $SRC_SCRIPT_PATH $DEST_SCRIPT_PATH

# Create the systemd service file
echo "[Unit]
Description=Collect File Usage Stats Service

[Service]
ExecStart=$DEST_SCRIPT_PATH -m=0
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/collectfileusagestats.service

# Reload the systemd manager configuration
sudo systemctl daemon-reload

# Enable your service, making it start on boot
sudo systemctl enable collectfileusagestats

# Start your service
sudo systemctl start collectfileusagestats