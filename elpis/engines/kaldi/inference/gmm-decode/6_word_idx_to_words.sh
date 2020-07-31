#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

echo "==== Translating Word Indexes to Words ===="
utils/int2sym.pl -f 5- \
    exp/tri1/graph/words.txt \
    data/infer/align-words-best-intkeys.ctm \
    > data/infer/align-words-best-wordkeys.ctm