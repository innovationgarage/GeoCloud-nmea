FROM ubuntu:18.04

RUN echo 3

RUN apt update
RUN apt install -y python3 python3-pip

RUN pip3 install libais==0.17
RUN pip3 install socket-tentacles
RUN pip3 install geocloud-nmea

ADD server.sh /server.sh

CMD ["/bin/bash", "/server.sh"]
