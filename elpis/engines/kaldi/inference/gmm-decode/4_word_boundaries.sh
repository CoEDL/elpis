#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

echo "==== Adding Word Boundaries to FST ===="
lattice-align-words \
    data/lang/phones/word_boundary.int \
    exp/tri1_online/final.mdl \
    ark,t:data/infer/1best-fst.tra \
    ark,t:data/infer/1best-fst-word-aligned.tra
