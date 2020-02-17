FROM ubuntu:18.04

ENV LANG C.UTF-8
RUN ["apt", "update"]
RUN ["apt", "install", "-y", "python3-pip"]
RUN ["pip3", "install", "flask"]
ADD *.py /