FROM ubuntu

COPY . /opt/OpenForge2/openforge
WORKDIR /opt/OpenForge2/openforge

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common &&\
    DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:openscad/releases &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y update &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y install openscad ruby &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y clean &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

