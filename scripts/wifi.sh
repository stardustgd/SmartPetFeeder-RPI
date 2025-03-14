#!/bin/bash

if [[ ! -z $CHECK_CONN_FREQ ]]
    then
        freq=$CHECK_CONN_FREQ
    else
        freq=120
fi


sleep 10
systemctl stop dnsmasq


while [[ true ]]; do
    echo "Checking internet connectivity ...";
    wget --spider --no-check-certificate 1.1.1.1 > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "Your device is already connected to the internet."
        echo "Skipping setting up Wifi-Connect Access Point. Will check again in $freq seconds."
    else
        echo "Your device is not connected to the internet."
        echo "Starting up Wifi-Connect.\n Connect to the Access Point and configure the SSID and Passphrase for the network to connect to.";
        /usr/local/sbin/wifi-connect -o 8080
    fi

    sleep $freq

done
