#! /bin/bash

echo "$CONFIG" > config.json
python3 /geocloud_nmea.py config.json
