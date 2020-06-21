FROM coedl/elpis:latest

# Install ESPnet dependencies
RUN apt-get update
RUN apt-get install -y cmake
RUN apt-get install -y sox
RUN apt-get install -y ffmpeg
RUN apt-get install -y flac
RUN apt-get install -y bc

WORKDIR /
RUN git clone https://github.com/persephone-tools/espnet.git
WORKDIR /espnet
RUN git checkout elpis
# Explicitly installing only the CPU version. We should update this to be an
# nvidia-docker image and install GPU-supported version of ESPnet.
WORKDIR /espnet/tools
RUN make KALDI=/kaldi CUPY_VERSION='' -j 4
