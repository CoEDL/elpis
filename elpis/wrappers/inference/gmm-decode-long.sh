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

echo "==== Finding Best Path (Transcription) ===="
lattice-1best \
    ark:exp/tri1_online/decode/lattices.ark \
    ark,t:data/infer/1best-fst.tra

echo "==== Adding Word Boundaries to FST ===="
lattice-align-words \
    data/lang/phones/word_boundary.int \
    exp/tri1_online/final.mdl \
    ark,t:data/infer/1best-fst.tra \
    ark,t:data/infer/1best-fst-word-aligned.tra

echo "==== Converting Lattice to CTM Format ===="
nbest-to-ctm \
    ark,t:data/infer/1best-fst-word-aligned.tra \
    data/infer/align-words-best-intkeys.ctm

echo "==== Translating Word Indexes to Words ===="
utils/int2sym.pl -f 5- \
    exp/tri1/graph/words.txt \
    data/infer/align-words-best-intkeys.ctm \
    > data/infer/align-words-best-wordkeys.ctm

# Activate Python 3.6.3 virtual environment
source /elpis/venv/bin/activate

# Now, wav.scp needs to be in segment form
# eg audio_id filename
echo "${recid} ${audio}" > ./data/infer/split1/1/wav.scp

echo "==== Converting CTM to Textgrid ===="
# python /kaldi-helpers/kaldi_helpers/output_scripts/ctm_to_textgrid.py \
python /elpis/elpis/wrappers/output/ctm_to_textgrid.py \
    --ctm data/infer/align-words-best-wordkeys.ctm \
    --wav data/infer/split1/1/wav.scp \
    --seg data/infer/split1/1/segments \
    --outdir data/infer

echo "==== Converting Textgrid to ELAN ===="
# python /kaldi-helpers/kaldi_helpers/output_scripts/textgrid_to_elan.py \
python /elpis/elpis/wrappers/output/textgrid_to_elan.py \
    --tg data/infer/utterance-0.TextGrid \
    --wav data/infer/wav.scp \
    --outfile data/infer/utterance-0.eaf

# REPORT OUTPUT (CTM is the only concise format)
echo "CTM output:"
cat ./data/infer/align-words-best-wordkeys.ctm

echo "==== Output the words from the CTM file as plain text ===="
awk 'BEGIN { ORS=" " }; { print $NF }' data/infer/align-words-best-wordkeys.ctm > data/infer/one-best-hypothesis.txt
