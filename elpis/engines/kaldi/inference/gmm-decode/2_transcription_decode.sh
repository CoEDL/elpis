#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

# Decodes all audio in the wav.scp path specified above
echo "==== Decoding (Transcription) ===="

steps/online/decode.sh \
    --config conf/decode.config \
    --cmd "$decode_cmd" \
    --nj 1 \
    exp/tri1/graph \
    data/infer \
    exp/tri1_online/decode

# Unzip lattice created by decode
gzip -dk exp/tri1_online/decode/lat.1.gz && \
    mv exp/tri1_online/decode/lat.1 exp/tri1_online/decode/lattices.ark
