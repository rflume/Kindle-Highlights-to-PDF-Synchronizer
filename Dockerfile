FROM ubuntu:xenial

LABEL author="Robin Flume"
LABEL version="1.0"

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y python \
                       python-pip \
                       mupdf-tools && \
    pip install --no-cache-dir PyMuPDF && \
    mkdir files

COPY synchronizer-docker.py /usr/src/app/synchronizer.py

ENTRYPOINT [ "python", "./synchronizer.py" ]
