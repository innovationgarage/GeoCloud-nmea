# GeoCloud-nmea

A thing wrapper around [libais](https://github.com/schwehr/libais/) to parse NMEA arriving over TCP streams,
and send it onwards as JSON over other TCP streams. It handles multiple concurrent sources and destinations, as well as both
listening for connections and connecting (with reconnect) to remove ports for both sources and destinations.
