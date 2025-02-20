# Wifi Connect Setup

## Initial Setup

Install [wifi-connect](https://github.com/balena-os/wifi-connect/) for aarch64 using the following command (check the releases tag to get the latest version):

`wget https://github.com/balena-os/wifi-connect/releases/download/v4.11.79/wifi-connect-aarch64-unknown-linux-gnu.tar.gz`

Extract the tar file:

`tar -xvzf wifi-connect-aarch64-unknown-linux-gnu.tar.gz`

Move `wifi-connect` to /usr/local/sbin/wifi-connect:

`mv wifi-connect /usr/local/sbin/`

Now we have to create a script that checks for internet connectivity. If we are connected, nothing needs to be done. If we aren't, start `wifi-connect`. Once we have the script set up, we can configure a systemd service to run this script on startup.

## Configuring systemd

Create a file called `/etc/systemd/system/wifi-connect.service`:

```ini
[Unit]
Description=WifiConnect
After=NetworkManager.service

[Service]
ExecStart=/home/pi/.scripts/wifi.sh
User=root
Group=root
Restart=on-failure
Environment="CHECK_CONN_FREQ=120"
Environment="VERBOSE=true"
Environment="PORTAL_SSID=SmartPetFeeder"
Type=idle
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

We can then turn on this service with the following commands:

```shell
systemctl reload-daemon
systemctl enable wifi-connect
```

## Troubleshooting

### Cannot start HTTP server

```shell
Starting HTTP server on 192.168.42.1:80
Error: Cannot start HTTP server on '192.168.42.1:80': Address already in use (os error 98)
```

This seems to be caused by a conflict between `wifi-connect` and `dnsmasq`. Adding the line `systemctl stop dnsmasq` in the script seems to fix the issue. If the issue still persists, there may be a conflict with `lighttpd`, since it uses port 80 as well. Disabling `lighttpd` with `systemctl disable lighttpd` fixes the issue.

### Captive Portal not opening

If the captive portal does not open, this is because you ran `wifi-connect` to run on a port other than 80. Using port 80 fixes the issue and the captive portal opens after connecting to the access point.
