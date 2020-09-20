#######################################################################
# Dockerfile to build Kaldi (speech recognition engine container      #
# image - based on Ubuntu + SRILM                                     #
#######################################################################

FROM ubuntu:18.04

########################## BEGIN INSTALLATION #########################

RUN apt-get update && apt-get install -y --fix-missing  \
    autoconf \
    automake \
    libtool-bin \
    make \
    gcc \
    g++ \
    gfortran \
    git \
    subversion \
    curl \
    wget \
    libjson-c3 \
    libjson-c-dev \
    zlib1g-dev \
    bzip2 \
    gsl-bin libgsl-dev \
    libatlas-base-dev \
    glpk-utils \
    libglib2.0-dev

# Python 2.7 required for building Kaldi
RUN apt-get update && apt-get install -y  \
    python2.7 \
    python-pip \
    python-yaml \
    python-simplejson \
    python-gi && \
    pip install ws4py==0.3.2 && \
    pip install tornado && \
    ln -s /usr/bin/python2.7 /usr/bin/python ; ln -s -f bash /bin/sh

# Add sox and graphviz for kaldi, vim and nano to edit scripts
RUN apt-get update && apt-get install -y \
    sox \
    graphviz \
    vim \
    zsh \
    unzip \
    tree \
    ffmpeg \
    ghostscript

# Install ESPnet dependencies (some may be covered above but listing all for
# the sake of completeness)
RUN apt-get install -y cmake \
    sox \
    ffmpeg \
    flac \
    bc

# Get and Build Kaldi
WORKDIR /

RUN echo "===> install Kaldi (latest from source)"  && \
    git clone -b 5.3 https://github.com/kaldi-asr/kaldi && \
    cd /kaldi/tools && \
    make && \
    ./install_portaudio.sh && \
    cd /kaldi/src && ./configure --mathlib=ATLAS --shared  && \
    sed -i '/-g # -O0 -DKALDI_PARANOID/c\-O3 -DNDEBUG' kaldi.mk && \
    make depend  && make && \
    cd /kaldi/src/online2 && make depend && make && \
    cd /kaldi/src/online2bin && make depend && make

COPY deps/srilm-1.7.2.tar.gz /kaldi/tools/srilm.tgz

WORKDIR /kaldi/tools

RUN apt-get install gawk && \
    chmod +x extras/* && \
    ./extras/install_liblbfgs.sh && \
    ./extras/install_srilm.sh && \
    chmod +x env.sh && \
    source ./env.sh

RUN apt-get install -y libssl-dev libsqlite3-dev libbz2-dev

WORKDIR /tmp

# Add python 3.6
RUN wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz && \
    tar xvf Python-3.6.6.tgz && \
    cd Python-3.6.6 && \
    ./configure --enable-optimizations --enable-loadable-sqlite-extensions && \
    make -j8 build_all && \
    make altinstall

# Add python packages and their dependencies
RUN apt-get install -y python3-dev python3-pip python3-certifi python3-venv

# Add a task runner
RUN curl -s https://taskfile.org/install.sh | sh && mv ./bin/task /bin/

# Add jq
RUN wget https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 && \
    chmod +x jq-linux64 && \
    mv jq-linux64 /usr/local/bin/jq

# Add node, npm and xml-js
RUN apt-get install -y nodejs build-essential npm && \
    #ln -s /usr/bin/nodejs /usr/bin/node && \
    npm install -g npm \
    hash -d npm \
    npm install -g xml-js

# Add moustache templates as mo
RUN curl -sSO https://raw.githubusercontent.com/tests-always-included/mo/master/mo && \
    chmod +x mo && \
    mv mo /usr/local/bin

# Clean up package manager
RUN apt-get clean autoclean

# Add random number generator to skip Docker building cache
ADD http://www.random.org/strings/?num=10&len=8&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new /uuid

# Elpis
WORKDIR /
RUN git clone --depth=1 https://github.com/CoEDL/elpis.git

# Elpis GUI
RUN git clone --depth=1 https://github.com/CoEDL/elpis-gui.git

# Example data
WORKDIR /tmp
RUN git clone --depth=1 https://github.com/CoEDL/toy-corpora.git

# Set up zsh & ENV variables
WORKDIR /root
RUN apt-get install zsh
RUN chsh -s /usr/bin/zsh root
RUN sh -c "$(wget -O- https://raw.githubusercontent.com/deluan/zsh-in-docker/master/zsh-in-docker.sh)" -- -t robbyrussell -p history-substring-search -p git
RUN echo "export FLASK_ENV=development" >> ~/.zshrc
RUN echo "export FLASK_APP=elpis" >> ~/.zshrc
RUN echo "export LC_ALL=C.UTF-8" >> ~/.zshrc
RUN echo "export LANG=C.UTF-8" >> ~/.zshhrc
RUN echo "export PATH=$PATH:/venv/bin:/kaldi/src/bin/" >> ~/.zshrc
RUN echo "alias run=\"flask run --host=0.0.0.0 --port=5000\"" >> ~/.zshrc
RUN cat ~/.zshrc >> ~/.bashrc

# Move ENV lines up. Putting here for now to build on top of cached builds
ENV FLASK_ENV='development'
ENV FLASK_APP='elpis'
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /elpis-gui
RUN npm install && \
    npm run build

WORKDIR /elpis
RUN /usr/bin/python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip3.6 install wheel pytest pylint && python setup.py develop

# Setting up ESPnet
WORKDIR /
RUN git clone https://github.com/persephone-tools/espnet.git
WORKDIR /espnet
RUN git checkout elpis
# Explicitly installing only the CPU version. We should update this to be an
# nvidia-docker image and install GPU-supported version of ESPnet.
WORKDIR /espnet/tools
RUN make KALDI=/kaldi CUPY_VERSION='' -j 4

WORKDIR /elpis

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]

EXPOSE 5000:5000
