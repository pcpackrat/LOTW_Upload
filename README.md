# LOTW Auto-Sync Service

A background service that connects directly to a Log4OM2 database, extracts amateur radio contacts that have not been uploaded to LOTW, safely formats them into ADIF, and uses the `tqsl` CLI in batch-mode to securely sign and upload them. It handles Log4OM2's internal JSON confirmation structure and updates the upload status automatically.

## Prerequisites (Debian 13)

Debian 13 (Trixie) enforces PEP-668 and blocks system-wide `pip` installations. You should install the required Python database driver and the `trustedqsl` package natively via `apt`:

```bash
sudo apt update
sudo apt install python3-pymysql trustedqsl
```

## Configuring TQSL (Headless Server)

The `tqsl` CLI will fail to sign logs if it doesn't have your ARRL certificate (`.p12` / `.tq6`) and a defined "Station Location". Because TQSL configuration is heavily tied to its graphical interface, doing this on a headless Debian server can be difficult.

**The easiest method:**
1. Open TQSL on your main desktop machine (Windows, Mac, or desktop Linux).
2. Fully configure your certificate and set up your **Station Location**.
3. Copy the hidden `.tqsl` configuration folder from your desktop to the Debian server:
   - **Windows:** `C:\Users\<YourUser>\.tqsl`
   - **Linux:** `~/.tqsl`
4. Place that `.tqsl` directory directly into the home folder of the user running the service (e.g., `/root/.tqsl` if running as root).
   - Alternatively, you can use TQSL's "Backup Station Location" feature and restore the `.tbk` file via command line.

## Script Configuration

Before installing, you must open `lotw_sync.py` and configure the database and TQSL settings at the top of the file:

```python
DB_HOST = "10.x.x.x"
DB_USER = "db_username"
DB_PASS = "db_password"
DB_NAME = "log4om2"

# You MUST update this to exactly match your TQSL Station Location name
TQSL_STATION_LOCATION = "Home"
```

## Installation

Once your configuration is set, run the included installation script. This will copy the necessary files to `/opt/lotw_sync/` and set up the systemd service and timer.

```bash
chmod +x install.sh
sudo ./install.sh
```

## Management

The script is triggered automatically by a systemd timer (default is every 1 hour). 

- **Check Timer Status:** `sudo systemctl status lotw_sync.timer`
- **Check Service Status:** `sudo systemctl status lotw_sync.service`
- **View Live Logs:** `sudo journalctl -u lotw_sync.service -f`
- **Trigger Manually:** `sudo systemctl start lotw_sync.service`

## Tools Included
- `check_status.py`: A manual diagnostic tool you can run directly (`python3 check_status.py`) to query the database and verify the exact LOTW upload status of your last 50 QSOs.
