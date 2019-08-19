#!/bin/bash

# Include Path
. ./path.sh

# COPY TRAINED MODEL
echo "==== Copying Pretrained Model ===="
cp -R ./exp/tri1 ./exp/tri

# "Usage: online-wav-gmm-decode-faster [options] wav-rspecifier model-in"
#        "fst-in word-symbol-table silence-phones transcript-wspecifier "


/kaldi/src/featbin/compute-cmvn-stats ark:data/infer/delta-feats.ark cmvn.scp

/kaldi/src/online2bin/online2-wav-gmm-latgen-faster \
    --global-cmvn-stats=cmvn.scp \
    ./exp/tri1/graph/HCLG.fst \
    ark:./data/infer/spk2utt \
    scp:./wav.scp \
    ark:./lattice.ark