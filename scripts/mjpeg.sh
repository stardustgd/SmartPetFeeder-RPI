#!/bin/bash

source ./scripts/config

nohup python src/mjpeg.py & 
nohup ssh -f -N -R $PORT:localhost:$PORT $VPS_HOSTNAME@$VPS_IP &
