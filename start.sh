#!/bin/bash

source .env

while true; do
    wget -q --spider http://google.com

    if [ $? -eq 0 ]; then
        echo "Running Smart Pet Feeder"
        python src/SmartPetFeeder.py $USER_EMAIL
        ./scripts/mjpeg.sh
        break
    else
        sleep 5
    fi
done
