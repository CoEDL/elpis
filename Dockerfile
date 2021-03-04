#######################################################################
# Dockerfile to build Kaldi (speech recognition engine container      #
# image - based on Ubuntu + SRILM                                     #
#######################################################################

FROM ubuntu:20.04

########################## BEGIN INSTALLATION #########################

ENV NUM_CPUS=1

ENV TZ=UTC

RUN export DEBIAN_FRONTEND="noninteractive" && apt-get update && apt-get install -y --fix-missing \
    autoconf \
    automake \
    bzip2 \
    curl \
    g++ \
    gcc \
    gfortran \
    git \
    glpk-utils \
    gsl-bin libgsl-dev \
    libatlas-base-dev \
    libglib2.0-dev \
    libjson-c-dev \
    libtool-bin \
    libssl-dev \
    libsqlite3-dev \
    libbz2-dev \
    make \
    software-properties-common \
    subversion \
    tree \
    unzip \
    vim \
    wget \
    zlib1g-dev \
    zsh

WORKDIR /tmp

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    PATH="/opt/pyenv/shims:/opt/pyenv/bin:$PATH" \
    PYENV_ROOT="/opt/pyenv" \
    PYENV_SHELL="zsh"

RUN echo "===> Install pyenv Python 3.8" && \
    git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT && \
    echo 'export PYENV_ROOT="/opt/pyenv"' >> ~/.zshrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc && \
    echo 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc && \
    eval "$(pyenv init -)" && \
    cat ~/.zshrc && \
    /bin/bash -c "source ~/.zshrc" && \
    pyenv install 3.8.2 && \
    rm -rf /tmp/*


########################## KALDI INSTALLATION #########################

RUN echo "===> Install Python 2.7 for Kaldi" && \
    add-apt-repository universe && \
    apt-get update && apt-get install -y  \
    python2.7 \
    python-yaml \
    python-simplejson \
    python-gi

RUN curl https://bootstrap.pypa.io/2.7/get-pip.py --output get-pip.py && \
    python2.7 get-pip.py

RUN pip2.7 install ws4py==0.3.2 && \
    pip2.7 install tornado

RUN ln -s /usr/bin/python2.7 /usr/bin/python ; ln -s -f bash /bin/sh

RUN echo "===> Install Kaldi dependencies" && \
    apt-get update && apt-get install -y \
    sox \
    graphviz \
    ghostscript\
    ffmpeg

WORKDIR /

RUN echo "===> install Kaldi (pinned at version 5.3)"  && \
    git clone -b 5.3 https://github.com/kaldi-asr/kaldi && \
    cd /kaldi/tools && \
    make -j$NUM_CPUS && \
    ./install_portaudio.sh && \
    cd /kaldi/src && ./configure --mathlib=ATLAS --shared  && \
    sed -i '/-g # -O0 -DKALDI_PARANOID/c\-O3 -DNDEBUG' kaldi.mk && \
    make depend -j$NUM_CPUS && make -j$NUM_CPUS && \
    cd /kaldi/src/online2 && make depend -j$NUM_CPUS && make -j$NUM_CPUS && \
    cd /kaldi/src/online2bin && make depend -j$NUM_CPUS && make -j$NUM_CPUS

COPY deps/srilm-1.7.2.tar.gz /kaldi/tools/srilm.tgz

WORKDIR /kaldi/tools

RUN apt-get install gawk && \
    chmod +x extras/* && \
    ./extras/install_liblbfgs.sh && \
    ./extras/install_srilm.sh && \
    chmod +x env.sh && \
    source ./env.sh

RUN apt-get install -y libssl-dev libsqlite3-dev libbz2-dev


########################## ESPNET INSTALLATION #########################

# Some ESPnet dependencies may be covered above but listing all for the sake of completeness
RUN echo "===> Install ESPnet dependencies" && \
    apt-get update && apt-get install -y cmake \
    sox \
    ffmpeg \
    flac \
    bc

WORKDIR /

# Setting up ESPnet for Elpis from Persephone repository
RUN git clone https://github.com/persephone-tools/espnet.git

WORKDIR /espnet

RUN git checkout elpis

# Explicitly installing only the CPU version. We should update this to be an
# nvidia-docker image and install GPU-supported version of ESPnet.
WORKDIR /espnet/tools

RUN echo "===> install ESPnet" && \
    make KALDI=/kaldi CUPY_VERSION='' -j $(nproc)


########################## DEV HELPERS INSTALLATION ####################

WORKDIR /tmp

# Add jq
RUN wget https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 && \
    chmod +x jq-linux64 && \
    mv jq-linux64 /usr/local/bin/jq

# Add node 15, npm and xml-js
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash - && apt-get update && apt-get install -y nodejs build-essential && \
    npm install -g npm \
    hash -d npm \
    npm install -g xml-js

# Clean up package manager
RUN apt-get clean autoclean

WORKDIR /root

# ZSH
RUN apt-get install zsh
RUN chsh -s /usr/bin/zsh root
RUN sh -c "$(wget -O- https://raw.githubusercontent.com/deluan/zsh-in-docker/master/zsh-in-docker.sh)" -- -t robbyrussell -p history-substring-search -p git

# Add random number generator to skip Docker building cache
ADD http://www.random.org/strings/?num=10&len=8&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new /uuid


########################## ELPIS INSTALLATION ########################

WORKDIR /

# Elpis
RUN pwd
RUN git clone --single-branch --branch welcome_update --depth=1 https://github.com/CoEDL/elpis.git
WORKDIR /elpis
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install poetry && poetry config virtualenvs.create false --local && \
    poetry install

WORKDIR /

# Elpis GUI
RUN ln -s /elpis/elpis/gui /elpis-gui
WORKDIR /elpis-gui
RUN npm install && \
    npm run build

WORKDIR /tmp

# Example data
RUN git clone --depth=1 https://github.com/CoEDL/toy-corpora.git


########################## RUN THE APP ##########################

# ENV vars for interactive running
RUN echo "export FLASK_ENV=development" >> ~/.zshrc
RUN echo "export FLASK_APP=elpis" >> ~/.zshrc
RUN echo "export LC_ALL=C.UTF-8" >> ~/.zshrc
RUN echo "export LANG=C.UTF-8" >> ~/.zshrc
RUN echo "export PATH=$PATH:/venv/bin:/kaldi/src/bin/" >> ~/.zshrc
RUN echo "alias run=\"poetry run flask run --host=0.0.0.0 --port=5000\"" >> ~/.zshrc
RUN cat ~/.zshrc >> ~/.bashrc

# ENV vars for non-interactive running
ENV FLASK_ENV='development'
ENV FLASK_APP='elpis'
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /elpis

ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

EXPOSE 5000:5000
EXPOSE 3000:3000
