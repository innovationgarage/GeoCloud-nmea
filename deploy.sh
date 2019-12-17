#! /bin/sh

export DOCKER_HOST=tcp://ymslanda.innovationgarage.tech:2375

docker build --tag innovationgarage/geocloud_nmea:latest .
docker push innovationgarage/geocloud_nmea:latest 
docker stack deploy -c docker-compose.yml geocloud_nmea
