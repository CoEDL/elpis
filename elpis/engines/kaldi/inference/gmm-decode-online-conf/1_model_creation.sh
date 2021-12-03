#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

# Apply cepstral mean variance normalisation and add delta features
echo "==== Applying CMVN ===="
/kaldi/src/featbin/apply-cmvn --utt2spk=ark:data/infer/utt2spk \
    scp:mfcc/cmvn_test.scp \
    scp:mfcc/raw_mfcc_infer.1.scp ark:- | \
    /kaldi/src/featbin/add-deltas ark:- ark:data/infer/delta-feats.ark

# Compute cepstral mean variance normalisation stats for online training
/kaldi/src/featbin/compute-cmvn-stats ark:data/infer/delta-feats.ark cmvn.scp

# This file's existence is required for online decoding, though it needs no content
echo "# dummy file" > ./conf/online_cmvn.conf

# Takes an offline model and creates and online variant
./steps/online/prepare_online_decoding.sh \
    --cmd "$train_cmd" \
    data/train \
    data/lang \
    exp/tri1 \
    exp/tri1_online

# Make the split dir with scp, utt2spk etc files
. $PWD/make_split.sh
