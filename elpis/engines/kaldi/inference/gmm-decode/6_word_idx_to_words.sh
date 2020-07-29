#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

echo "==== Translating Word Indexes to Words ===="
utils/int2sym.pl -f 5- \
    exp/tri1/graph/words.txt \
    data/infer/align-words-best-intkeys.ctm \
    > data/infer/align-words-best-wordkeys.ctm

# Activate Python 3.6.3 virtual environment
source /venv/bin/activate

# Now, wav.scp needs to be in segment form
# eg audio_id filename
echo "${recid} ${audio}" > ./data/infer/split1/1/wav.scp
