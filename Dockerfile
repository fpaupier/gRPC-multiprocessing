FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install -y wget python3.8 python3-pip python3-dev

# OpenCV requirements
RUN python3.8 -m pip install --upgrade pip
RUN apt update && apt install -y libsm6 libxext6 libxrender-dev libgl1-mesa-glx

# Tesseract requirements
RUN apt update && apt install -y libleptonica-dev tesseract-ocr libtesseract-dev

# gRPC healthcheck
RUN wget https://github.com/fullstorydev/grpcurl/releases/download/v1.8.2/grpcurl_1.8.2_linux_x86_64.tar.gz -O /grpcurl.tar.gz
RUN tar -xvzf /grpcurl.tar.gz
RUN chmod +x grpcurl && mv grpcurl /usr/local/bin/grpcurl && rm /grpcurl.tar.gz

COPY ./requirements.txt /requirements.txt

RUN python3.8 -m pip install --upgrade pip && python3.8 -m pip install -r /requirements.txt
