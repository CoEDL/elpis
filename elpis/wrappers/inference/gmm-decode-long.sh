#!/bin/bash

# Include Path
. ./path.sh

# AUDIO --> FEATURE VECTORS
echo "==== Extracting Feature Vectors ===="
steps/make_mfcc.sh --nj 1 data/infer exp/make_mfcc/infer mfcc

echo "==== Applying CMVN ===="
apply-cmvn --utt2spk=ark:data/infer/utt2spk \
    scp:mfcc/cmvn_test.scp \
    scp:mfcc/raw_mfcc_infer.1.scp ark:- | \
    add-deltas ark:- ark:data/infer/delta-feats.ark

# TRAINED GMM-HMM + FEATURE VECTORS --> LATTICE
echo "==== Producing Lattice ===="
gmm-latgen-faster \
    --word-symbol-table=exp/tri1/graph/words.txt \
    exp/tri1/final.mdl \
    exp/tri1/graph/HCLG.fst \
    ark:data/infer/delta-feats.ark \
    ark,t:data/infer/lattices.ark

./steps/online/prepare_online_decoding.sh \
    data/train \
    data/lang \
    exp/tri \
    exp/tri/final.mdl \
    exp/tri_online

/kaldi/src/featbin/compute-cmvn-stats ark:data/infer/delta-feats.ark cmvn.scp

/kaldi/src/online2bin/online2-wav-gmm-latgen-faster \
    --model=exp/tri_online/final.mdl \
    --global-cmvn-stats=cmvn.scp \
    exp/tri/graph/HCLG.fst \
    ark:data/infer/spk2utt \
    scp:data/infer/wav.scp \
    ark:data/infer/lattices.ark