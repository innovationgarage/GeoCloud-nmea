#! /bin/bash

echo "$CONFIG" > config.json
python3 geocloud-nmea config.json
