#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

# REPORT OUTPUT (CTM is the only concise format)
echo "==== CTM OUTPUT ===="
cat ./data/infer/align-words-best-wordkeys.ctm

awk 'BEGIN { ORS=" " }; { print $NF }' data/infer/align-words-best-wordkeys.ctm > data/infer/one-best-hypothesis.txt
