FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt install && apt install software-properties-common -y
RUN apt-get install python3.8 python3-pip -y
RUN apt-get install -y python-dev

# OpenCV requirements
RUN python3.8 -m pip install --upgrade pip
RUN apt-get install -y libsm6 libxext6 libxrender-dev libgl1-mesa-glx


# gRPC healthcheck
COPY ./resources/grpcurl_1.8.0_linux_x86_64.tar.gz /grpcurl_1.8.0_linux_x86_64.tar.gz
RUN tar -xvzf /grpcurl_1.8.0_linux_x86_64.tar.gz
RUN chmod +x grpcurl
RUN mv grpcurl /usr/local/bin/grpcurl

COPY ./requirements.txt /requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip python3.8 -m pip install --upgrade pip && python3.8 -m pip install -r /requirements.txt
