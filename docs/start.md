# Smart Pet Feeder Startup Script

## Configuring systemd

```ini
[Unit]
Description=SmartPetFeeder
After=NetworkManager.service

[Service]
ExecStart=/home/pi/SmartPetFeeder-RPI/start.sh
User=root
Group=root
Restart=on-failure
Type=idle
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

```
