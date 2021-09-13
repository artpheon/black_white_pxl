# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

LABEL name="Artur N."

LABEL maintainer="idcdtokms@gmail.com"

RUN apt-get update && apt-get -y upgrade

RUN apt-get -y install -y wget sudo bash vim software-properties-common

RUN sudo apt install -y python3-opencv && pip install --upgrade pip

RUN pip install flask opencv-python numpy

WORKDIR /var/hrobbin/

COPY ./src/ /var/hrobbin/

RUN chmod 777 /var/hrobbin

RUN mkdir /var/hrobbin/tmp

EXPOSE 8090

ENTRYPOINT ["/bin/bash"]