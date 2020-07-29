#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

# REPORT OUTPUT (CTM is the only concise format)
echo "CTM output:"
cat ./data/infer/align-words-best-wordkeys.ctm

echo "==== Output the words from the CTM file as plain text ===="
awk 'BEGIN { ORS=" " }; { print $NF }' data/infer/align-words-best-wordkeys.ctm > data/infer/one-best-hypothesis.txt
