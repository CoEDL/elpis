#######################################################################
# Dockerfile to build Kaldi (speech recognition engine container      #
# image - based on Ubuntu + SRILM                                     #
#######################################################################

FROM ubuntu:18.04

########################## BEGIN INSTALLATION #########################

RUN apt-get update && apt-get install -y  \
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
    nano \
    zsh \
    unzip \
    tree \
    ffmpeg

# Get and Build Kaldi
WORKDIR /

RUN echo "===> install Kaldi (latest from source)"  && \
    git clone https://github.com/kaldi-asr/kaldi && \
    cd /kaldi/tools && \
    make && \
    ./install_portaudio.sh && \
    cd /kaldi/src && ./configure --shared && \
    sed -i '/-g # -O0 -DKALDI_PARANOID/c\-O3 -DNDEBUG' kaldi.mk && \
    make depend  && make && \
    cd /kaldi/src/online && make depend && make

COPY srilm-1.7.2.tar.gz /kaldi/tools/srilm.tgz

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
    make -j8 && \
    make altinstall

# Add python packages and their dependencies
RUN apt-get install -y python3-dev python3-pip python3-certifi python3-venv && \
    pip3.6 install numpy pympi-ling praatio pydub

# Add a task runner
RUN curl -s https://taskfile.org/install.sh | sh && mv ./bin/task /bin/

# Add jq
RUN wget https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 && \
    chmod +x jq-linux64 && \
    mv jq-linux64 /usr/local/bin/jq

# Add node, npm and xml-js
RUN apt-get install -y nodejs build-essential npm && \
    #ln -s /usr/bin/nodejs /usr/bin/node && \
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
RUN git clone https://github.com/CoEDL/elpis.git

WORKDIR /elpis
RUN git submodule update --init --recursive && cd elpis-gui && git pull origin master
RUN npm build

# Get Kaldi-Helpers and install it
RUN cd /tmp && git clone https://github.com/CoEDL/kaldi-helpers.git /kaldi-helpers
RUN cd /kaldi-helpers && python3.6 setup.py install

# Get example corpora
RUN cd /tmp && git clone https://github.com/CoEDL/toy-corpora.git && \
    mv toy-corpora/* /kaldi-helpers/resources/corpora/

RUN cd /tmp && sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

WORKDIR /kaldi-helpers

RUN echo "FLASK_ENV=development" >> ~/.bashrc
RUN echo "FLASK_APP=elpis" >> ~/.bashrc
RUN echo "export LC_ALL=C.UTF-8" >> ~/.bashrc
RUN echo "export LANG=C.UTF-8" >> ~/.bashrc

# Move ENV lines up. Putting here for now so I can build on top of cached builds
ENV FLASK_ENV='development'
ENV FLASK_APP='elpis'
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /kaldi-helpers
RUN python3.6 setup.py bdist_egg && \
    cp dist/kaldi_helpers-0.23-py3.6.egg /usr/local/lib/python3.6/site-packages/kaldi_helpers-0.2-py3.6.egg

WORKDIR /elpis/elpis-gui
RUN npm install && \
    npm run build

WORKDIR /elpis
RUN pip3.6 install appdirs pystache && \
    pip3.6 install -r requirements.txt

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]

EXPOSE 5000:5000
EXPOSE 8008:8008
