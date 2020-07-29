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

# Assuming we are decoding a single utterance still

# Manipulate the wav.scp file in the first (and only) split
line=$(head -n 1 ./data/infer/spk2utt)
utt=` echo ${line} | cut -d ' ' -f 2`
spk=` echo ${line} | cut -d ' ' -f 1` # this was seg
audio="audio.wav"
length=`sox --i -D ${audio}`
recid="decode"

# Prepare the split dir
splitDir=./data/infer/split1/
if [[ -d $splitDir ]]; then rm -r $splitDir; fi
mkdir -p "$splitDir/1"

# Argh.. the wav.scp file here should be in {utterance_id} to {audio_file} form
# unlike other usage which requires {audio_id} to {audio_file} format
# (such as below when we convert ctm to textgrid)
echo "${utt} ${audio}" > ./data/infer/split1/1/wav.scp
echo "${utt} ${spk}" > ./data/infer/split1/1/utt2spk
echo "${spk} ${utt}" > ./data/infer/split1/1/spk2utt
echo "${utt} ${recid} 0.00 ${length}" > ./data/infer/split1/1/segments
