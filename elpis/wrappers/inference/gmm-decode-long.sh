#!/bin/bash

# Include Path
. ./path.sh

# COPY TRAINED MODEL
echo "==== Copying Pretrained Model ===="
cp -R ./exp/tri1 ./exp/tri

# "Usage: online-wav-gmm-decode-faster [options] wav-rspecifier model-in"
#        "fst-in word-symbol-table silence-phones transcript-wspecifier "

./online-wav-gmm-decode-faster \
    --rt-min=0.3 --rt-max=0.5 \
    --max-active=4000 \
    --beam=12.0 \
    --acoustic-scale=0.0769 \
    scp:wav.scp \
    ./exp/tri/final.mdl \
    ./exp/tri/graph/HCLG.fst \
    ./exp/tri/graph/words.txt \
    '1:2' \
    ark,t:trans.txt \
    ark,t:ali.txt
