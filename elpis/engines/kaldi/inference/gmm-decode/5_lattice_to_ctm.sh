#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

echo "==== Converting Lattice to CTM Format ===="
nbest-to-ctm \
    ark,t:data/infer/1best-fst-word-aligned.tra \
    data/infer/align-words-best-intkeys.ctm
