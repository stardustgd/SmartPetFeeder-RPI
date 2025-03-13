#!/bin/bash

cd $HOME/SmartPetFeeder-RPI

source .env

while true; do
    wget -q --spider http://google.com

    if [ $? -eq 0 ]; then
        echo "Starting camera"
        ./scripts/mjpeg.sh &
        
        echo "Running Smart Pet Feeder"
        source ./.venv/bin/activate
        python src/SmartPetFeeder.py $USER_EMAIL &
        deactivate

        break
    else
        sleep 5
    fi
done

# Keep the script running
sleep infinity
