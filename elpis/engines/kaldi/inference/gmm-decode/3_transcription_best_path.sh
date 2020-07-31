#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

echo "==== Finding Best Path (Transcription) ===="
lattice-1best \
    ark:exp/tri1_online/decode/lattices.ark \
    ark,t:data/infer/1best-fst.tra
