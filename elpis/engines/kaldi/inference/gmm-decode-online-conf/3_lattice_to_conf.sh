#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

echo "==== Lattice to Conf ===="

# Enable setting acoustic scale by ENV
# eg run this as `ACOUSTIC_SCALE=2 gmm-deccode-conf.sh`
# seems that 1/10 or 1/12 is a standard setting but idkw
# TODO add a GUI setting for this
acoustic_scale="${ACOUSTIC_SCALE:-0.1}"

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
