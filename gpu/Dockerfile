#######################################################################
# Dockerfile to build Kaldi (speech recognition engine container      #
# image - based on Ubuntu + SRILM                                     #
#######################################################################

FROM ubuntu:20.04

########################## BEGIN INSTALLATION #########################

ENV PYTHON_VERSION 3.8.6
ENV PYTHON_VER 3.8

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

RUN echo "===> Install Python 3.8 packages" && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.8-dev python3.8-venv


########################## KALDI INSTALLATION #########################

RUN echo "===> Install Python 2.7 for Kaldi" && \
    add-apt-repository universe && \
    apt-get update && apt-get install -y  \
    python2.7 \
    python-yaml \
    python-simplejson \
    python-gi

RUN curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py && \
    python2 get-pip.py

RUN pip install ws4py==0.3.2 && \
    pip install tornado

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
    make -j`nproc` && \
    ./install_portaudio.sh && \
    cd /kaldi/src && ./configure --mathlib=ATLAS --shared  && \
    sed -i '/-g # -O0 -DKALDI_PARANOID/c\-O3 -DNDEBUG' kaldi.mk && \
    make depend -j`nproc` && make -j`nproc` && \
    cd /kaldi/src/online2 && make depend -j`nproc` && make -j`nproc` && \
    cd /kaldi/src/online2bin && make depend -j`nproc` && make -j`nproc`

COPY deps/srilm-1.7.2.tar.gz /kaldi/tools/srilm.tgz

WORKDIR /kaldi/tools

RUN apt-get install gawk && \
    chmod +x extras/* && \
    ./extras/install_liblbfgs.sh && \
    ./extras/install_srilm.sh && \
    chmod +x env.sh && \
    source ./env.sh

RUN apt-get install -y libssl-dev libsqlite3-dev libbz2-dev

########################## DEV HELPERS INSTALLATION ####################

WORKDIR /tmp

# Add jq
RUN wget https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 && \
    chmod +x jq-linux64 && \
    mv jq-linux64 /usr/local/bin/jq

# Add node 15, npm and xml-js
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get update && apt-get install -y nodejs build-essential && \
    #ln -s /usr/bin/nodejs /usr/bin/node && \
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

########################## CUDA INSTALLATION ####################

# TODO: if possible, make one dockerfile for CPU and GPU together, one day…

ENV CUDA_VER 10.1

RUN apt-get update && apt-get install -y --no-install-recommends gnupg2 curl ca-certificates && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get purge --autoremove -y curl && \
    rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 10.1.168

ENV CUDA_PKG_VERSION 10-1=$CUDA_VERSION-1

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION \
        cuda-compat-10-1 && \
    ln -s cuda-10.1 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.1 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=396,driver<397 brand=tesla,driver>=410,driver<411"

ENV CUDA_HOME /usr/local/cuda

## FROM CUDA 10.1 runtime [https://gitlab.com/nvidia/cuda/blob/ubuntu18.04/10.1/runtime/Dockerfile]

ENV NCCL_VERSION 2.7.8

RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-libraries-$CUDA_PKG_VERSION \
        cuda-nvtx-$CUDA_PKG_VERSION \
        libnccl2=$NCCL_VERSION-1+cuda10.1 && \
    apt-mark hold libnccl2 && \
    rm -rf /var/lib/apt/lists/*

## FROM CUDA 10.1 devel [https://gitlab.com/nvidia/cuda/blob/ubuntu18.04/10.1/devel/Dockerfile]

RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-nvml-dev-$CUDA_PKG_VERSION \
        cuda-command-line-tools-$CUDA_PKG_VERSION \
        cuda-nvprof-$CUDA_PKG_VERSION \
        cuda-npp-dev-$CUDA_PKG_VERSION \
        cuda-libraries-dev-$CUDA_PKG_VERSION \
        cuda-minimal-build-$CUDA_PKG_VERSION \
        libcublas-dev=10.2.1.243-1 \
        libnccl-dev=2.7.8-1+cuda10.1 && \
    apt-mark hold libnccl-dev &&  \
    rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libcublas-dev

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs

## FROM CUDA 10.1-CUDNN 7 devel

ENV CUDNN_VERSION 7.6.0.64
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
            libcudnn7=$CUDNN_VERSION-1+cuda10.1 \
            libcudnn7-dev=$CUDNN_VERSION-1+cuda10.1 && \
    apt-mark hold libcudnn7 && \
    rm -rf /var/lib/apt/lists/*

# NOTE: needed to manually add this.
# FROM https://github.com/NVIDIA/nvidia-docker/issues/1256
# FROM https://forums.developer.nvidia.com/t/how-to-use-cuda-compatibility-package-to-use-a-newer-driver-on-an-older-kernel-module/77533
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:/usr/local/cuda-10.1/compat/:$LD_LIBRARY_PATH

########################## ELPIS INSTALLATION ########################

WORKDIR /

# Elpis
RUN git clone --depth=1 https://github.com/CoEDL/elpis.git
WORKDIR /elpis
RUN /usr/bin/python3.8 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install poetry && poetry config virtualenvs.create false --local && \
    poetry install

# # Recent version of pip is needed to install llvmlite (needed by librosa) flawlessly.
# RUN pip$PYTHON_VER install --upgrade pip
# # Needed because numba (for librosa) needs numpy but it seems not installed automatically with pip…  Also, llvmlite version installed by librosa won’t satisfy requirements for numba, without flexibility, so it is better to install them before…
# RUN pip$PYTHON_VER install numpy numba
# RUN pip$PYTHON_VER install wheel pytest pylint && python$PYTHON_VER setup.py develop

WORKDIR /

# Elpis GUI
RUN ln -s /elpis/elpis/gui /elpis-gui
WORKDIR /elpis-gui
RUN npm install && \
    npm run build

# For /elpis (elan conversion)
RUN npm install xslt3

WORKDIR /tmp

# Example data
RUN git clone --depth=1 https://github.com/CoEDL/toy-corpora.git

########################## ESPNET INSTALLATION #########################

# Some ESPnet dependencies may be covered above but listing all for the sake of completeness
RUN echo "===> Install ESPnet dependencies" && \
    apt-get update && apt-get install -y cmake \
    sox \
    ffmpeg \
    flac \
    bc

WORKDIR /

# Because Espnet dependencies need GCC compiler version ≤ 8.
RUN apt -y install gcc-8 g++-8 && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 8 && \
    update-alternatives --config gcc

# Pinned and tested version (from forked repository).
RUN git clone --depth=1 -b elpis https://github.com/persephone-tools/espnet.git

# Necessary installers (from main repository) for Anaconda and Cuda stuffs.
RUN git clone --depth=1 https://github.com/espnet/espnet /tmp/espnet
RUN mv /tmp/espnet/tools/setup_anaconda.sh /espnet/tools/setup_anaconda.sh
RUN mv /tmp/espnet/tools/setup_cuda_env.sh /espnet/tools/setup_cuda_env.sh
RUN rm -rf /tmp/espnet

WORKDIR /espnet/tools

# FROM ESPnet devel [https://github.com/espnet/espnet/blob/master/docker/prebuilt/devel/Dockerfile]
RUN echo "ESPnet build with CUDA" && \
    # Docker containers cannot load cuda libs during build.
    # So, their checks on cuda packages are disabled.
    sed -i '200s|install.py|install.py --no-cuda --no-cupy |' Makefile && \
    export CFLAGS="-I${CUDA_HOME}/include ${CFLAGS}" && \
    MY_OPTS="CUDA_VERSION=${CUDA_VER}" && \
    . ./setup_cuda_env.sh /usr/local/cuda;  \
    if [ "${CUDA_VER}" = "10.1" ]; then \
        # warpctc is not supported from Pytorch 1.3.1
        MY_OPTS="${MY_OPTS} TH_VERSION=1.3.1";  \
    fi; \
    echo "Make with options ${MY_OPTS}" && \
    ln -s /kaldi ./ && \
    ./setup_anaconda.sh /miniconda espnet 3.7.4 && \
    make KALDI=/kaldi ${MY_OPTS} -j`nproc`

# There will be a warning saying that cuda *seems* not to be available in torch, but it will be: just don't forget to run the image with "--gpus all" and it will be available. During docker building, nvidia-smi and cuda stuff are not fully available, but they are during runtime; the only way I found to force this visibility during building is described (here)[https://stackoverflow.com/questions/59691207/docker-build-with-nvidia-runtime], but I did not try it because it is quite invasive…

# NOTE: needed because /espnet/egs/elpis/asr1/path.sh needs venv (and /miniconda is not so easily movable, to be checked one day…)
RUN ln -s /miniconda/envs/espnet /espnet/tools/venv

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
