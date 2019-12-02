#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh


# Add online binaries to PATH
export PATH=$PATH:/kaldi/src/online2bin

# Extract feature vectors for online training
echo "==== Extracting Feature Vectors ===="
steps/make_mfcc.sh --nj 1 data/infer exp/make_mfcc/infer mfcc

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

# Manipulate the wav.scp file in the first (and only) split
line=$(head -n 1 ./data/infer/spk2utt) && \
 utt=` echo ${line} | cut -d ' ' -f 2` &&
 echo "${utt} ./20030518Abui2PieterFrogDogBoy.wav" > ./data/infer/split1/1/wav.scp

# Decodes all audio in the wav.scp path specified above
steps/online/decode.sh \
    --config conf/decode.config \
    --cmd "$decode_cmd" \
    --nj 1 \
    exp/tri1/graph \
    data/infer \
    exp/tri1_online/decode
