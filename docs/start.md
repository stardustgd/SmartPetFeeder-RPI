# Smart Pet Feeder Startup Script

## Configuring systemd

Create a file called `/etc/systemd/system/smart-pet-feeder.service`:

```ini
[Unit]
Description=SmartPetFeeder
After=network-online.target NetworkManager.service
Wants=network-online.target

[Service]
ExecStart=/home/pi/SmartPetFeeder-RPI/start.sh
User=pi
Group=pi
Restart=on-failure
Type=idle
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
