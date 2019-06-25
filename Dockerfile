FROM ubuntu:18.04

RUN echo 1

RUN apt update
RUN apt install -y python3 python3-pip

RUN pip3 install libais==0.17

ADD server.sh /server.sh
ADD geocloud_nmea.py /geocloud_nmea.py

CMD ["/bin/bash", "/server.sh"]