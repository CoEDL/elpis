#!/bin/bash

# Copyright: University of Queensland, 2019
# Contributors:
#               Joshua Meyer - (2016)
#               Scott Heath - (University of Queensland, 2018)
#               Nicholas Lambourne - (University of Queensland, 2018)
#
#    This script is meant to demonstrate how an existing GMM-HMM
#    model and its corresponding HCLG graph, build via Kaldi,
#    can be used to decode new audio files.
#    Although this script takes no command line arguments, it assumes
#    the existance of a directory (./transcriptions) and an scp file
#    within that directory (./transcriptions/wav.scp). For more on scp
#    files, consult the official Kaldi documentation.

# INPUT:
#       audio.wav
#       data/
#       infer/          <= these need to be created
#           wav.scp
#           utt2spk
#           spk2utt
#           text        <= put a transcription here for quick comparison against generated one
#
#    config/
#        mfcc.conf
#
#    exp/
#        tri/
#            final.mdl
#
#            graph/
#                HCLG.fst
#                words.txt

# OUTPUT:
#    data/
#       infer/
#            feats.ark
#            feats.scp
#            delta-feats.ark
#            lattices.ark
#            one-best.tra
#            one-best-hypothesis.txt



. ./path.sh
# make sure you include the path to the gmm bin(s)
# the following two export commands are what my path.sh script contains:
# export PATH=$PWD/utils/:$PWD/../../../src/bin:$PWD/../../../tools/openfst/bin:$PWD/../../../src/fstbin/:$PWD/../../../src/gmmbin/:$PWD/../../../src/featbin/:$PWD/../../../src/lm/:$PWD/../../../src/sgmmbin/:$PWD/../../../src/fgmmbin/:$PWD/../../../src/latbin/:$PWD/../../../src/nnet2bin/:$PWD:$PATH
# export LC_ALL=C

# Make the split dir with scp, utt2spk etc files
. $PWD/make_split.sh

echo "==== Using GMM Decode Conf ===="

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

echo "==== Lattice to Conf ===="

# Enable setting acoustic scale by ENV
# eg run this as `ACOUSTIC_SCALE=2 gmm-deccode-conf.sh`
# seems that 1/10 or 1/12 is a standard setting but idkw
# TODO add a GUI setting for this
acoustic_scale="${ACOUSTIC_SCALE:-0.1}"
echo "Using acoustic scale: ${acoustic_scale}"

lattice-align-words \
  data/lang/phones/word_boundary.int \
  exp/tri1/final.mdl \
  ark:data/infer/lattices.ark \
  ark:- | \

lattice-to-ctm-conf --acoustic-scale=$acoustic_scale \
  ark:- - | \

utils/int2sym.pl -f 5 \
    exp/tri1/graph/words.txt \
    > data/infer/ctm_with_conf.ctm

# Now, wav.scp needs to be in segment form
# eg audio_id filename
audio_filename=$(<./data/infer/audio_meta.txt)
echo "decode ${audio_filename}" > ./data/infer/split1/1/wav.scp

echo "==== CTM output ===="
awk  -F" " 'BEGIN { ORS=" " }; {print $(NF-1)}' \
  data/infer/ctm_with_conf.ctm \
  > data/infer/one-best-hypothesis.txt

# Add a newline to the file
echo >> data/infer/one-best-hypothesis.txt

cat data/infer/one-best-hypothesis.txt

echo "==== Build the Elan file ===="
python3 /elpis/elpis/engines/common/output/ctm_to_elan.py \
    --ctm data/infer/ctm_with_conf.ctm \
    --wav data/infer/split1/1/wav.scp \
    --seg data/infer/split1/1/segments \
    --outdir data/infer \
    --confidence

