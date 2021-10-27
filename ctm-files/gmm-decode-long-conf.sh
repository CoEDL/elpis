#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh


# Add online binaries to PATH (this can be removed after testing - has been added to elpis path.sh)
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

# Decodes all audio in the wav.scp path specified above
echo "==== Decoding (Transcription) ===="

steps/online/decode.sh \
    --config conf/decode.config \
    --cmd "$decode_cmd" \
    --nj 1 \
    exp/tri1/graph \
    data/infer \
    exp/tri1_online/decode

# Unzip lattice created by decode
gzip -dk exp/tri1_online/decode/lat.1.gz && \
    mv exp/tri1_online/decode/lat.1 exp/tri1_online/decode/lattices.ark

echo "==== Lattice to Conf ===="

# Enable setting acoustic scale by ENV
# eg run this as `ACOUSTIC_SCALE=2 gmm-deccode-conf.sh`
# seems that 1/10 or 1/12 is a standard setting but idkw
# TODO add a GUI setting for this
acoustic_scale_default=0.1
acoustic_scale="${ACOUSTIC_SCALE:-acoustic_scale_default}"

lattice-align-words \
    data/lang/phones/word_boundary.int \
    exp/tri1_online/final.mdl \
    ark:exp/tri1_online/decode/lattices.ark \
    ark:- | \

lattice-to-ctm-conf --acoustic-scale=$acoustic_scale \
  ark:- - | \

utils/int2sym.pl -f 5 \
    exp/tri1/graph/words.txt \
    > data/infer/ctm_with_conf.ctm

# Now, wav.scp needs to be in segment form
# eg audio_id filename
echo "${recid} ${audio}" > ./data/infer/split1/1/wav.scp

echo "==== CTM output ===="
awk  -F" " 'BEGIN { ORS=" " }; {print $(NF-1)}' \
  data/infer/ctm_with_conf.ctm \
  > data/infer/one-best-hypothesis.txt

# Add a newline to the file
echo >> data/infer/one-best-hypothesis.txt

cat data/infer/one-best-hypothesis.txt

echo "==== Build the Elan file ===="
"${POETRY_PATH}/bin/python" /elpis/elpis/engines/common/output/ctm_to_elan.py \
    --ctm data/infer/ctm_with_conf.ctm \
    --wav data/infer/split1/1/wav.scp \
    --seg data/infer/split1/1/segments \
    --outdir data/infer \
    --confidence

