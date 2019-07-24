# GeoCloud-nmea

A thing wrapper around [libais](https://github.com/schwehr/libais/) to parse NMEA arriving over TCP streams,
and send it onwards as JSON over other TCP streams. It handles multiple concurrent sources and destinations, as well as both
listening for connections and connecting (with reconnect) to remote ports for both sources and destinations.

Usage:

    python geocloud_nmea.py config.json

## Docker

    docker build --tag geocloud-nmea .

    docker run \
      -p 1024:1024 \
      -p 1025:1025 \
      -e 'CONFIG={"connections": [{"handler": "source", "type": "listen", "address": "tcp:1024"},{"handler": "destination", "type": "listen", "address": "tcp:1025"},{"handler": "destination", "type": "connect", "address": "tcp:localhost:1026"}]}' \
      geocloud-nmea
