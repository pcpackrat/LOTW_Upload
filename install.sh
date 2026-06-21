#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

INSTALL_DIR="/opt/lotw_sync"
SERVICE_FILE="/etc/systemd/system/lotw_sync.service"
TIMER_FILE="/etc/systemd/system/lotw_sync.timer"

echo "Installing LOTW Auto-Sync Service to $INSTALL_DIR..."

# Create directory
mkdir -p "$INSTALL_DIR"

# Copy python script
cp lotw_sync.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/lotw_sync.py"

# Copy systemd files
cp lotw_sync.service "$SERVICE_FILE"
chmod 644 "$SERVICE_FILE"

cp lotw_sync.timer "$TIMER_FILE"
chmod 644 "$TIMER_FILE"

# Reload systemd and enable/start the timer
echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Enabling and starting the lotw_sync timer..."
systemctl enable lotw_sync.timer
systemctl start lotw_sync.timer

echo "Installation complete!"
echo "Check the timer status with: systemctl status lotw_sync.timer"
echo "View the logs with: journalctl -u lotw_sync.service -f"
