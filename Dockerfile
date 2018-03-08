FROM ubuntu

COPY . /opt/OpenForge2/openforge
WORKDIR /opt/OpenForge2/openforge

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common &&\
    DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:openscad/releases &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y update &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y install openscad ruby &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y clean &&\
    ln -s /opt/OpenForge2/openforge/openforge /usr/lib/python3/dist-packages &&\
    ln -s /opt/OpenForge2/openforge/bin/* /usr/local/bin &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-dev python3-pip cmake cmake-curses-gui git sudo wget &&\
    cd /opt &&\
    wget http://download.blender.org/source/blender-2.77a.tar.gz &&\
    tar -zxvf blender-2.77a.tar.gz &&\
    cd blender-2.77a &&\
    ./build_files/build_environment/install_deps.sh --no-confirm &&\
    cd .. &&\
    mkdir cmake-blender &&\
    cd cmake-blender &&\
    cmake -D WITH_CYCLES=OFF -D WITH_PYTHON_INSTALL=OFF -D WITH_PLAYER=OFF -D WITH_PYTHON_MODULE=ON -D WITH_INSTALL_PORTABLE=OFF ../blender-2.77a &&\
    make &&\
    make install &&\
    mv /usr/local/PYTHON_SITE_PACKAGES-NOTFOUND/* /usr/lib/python3.5/ &&\
    cd /opt &&\
    rm blender-2.77a.tar.gz &&\
    rm -rf blender-2.77a &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y clean &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#    git clone http://git.blender.org/blender.git &&\
#    cd blender &&\
#    git checkout v2.76b && \
#    git submodule update --init --recursive &&\
#    git submodule foreach git checkout master &&\
#    git submodule foreach git pull --rebase origin master &&\
#    DEBIAN_FRONTEND=noninteractive true | ./build_files/build_environment/install_deps.sh &&\
#    cmake -D WITH_CYCLES=OFF -D WITH_PYTHON_INSTALL=OFF -D WITH_PLAYER=OFF -D WITH_PYTHON_MODULE=ON -D WITH_INSTALL_PORTABLE=OFF ../blender-2.77a


