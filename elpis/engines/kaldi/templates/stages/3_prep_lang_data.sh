#!/bin/bash

. ./path.sh || exit 1
. ./cmd.sh || exit 1

nj=1       # number of parallel jobs - 1 is perfect for such a small data set
lm_order=1 # language model order (n-gram quantity) - 1 is enough for digits grammar

echo
echo "===== PREPARING LANGUAGE DATA ====="
echo

# Needs to be prepared by hand (or using self written scripts):
#
# lexicon.txt           [<word> <phone 1> <phone 2> ...]
# nonsilence_phones.txt    [<phone>]
# silence_phones.txt    [<phone>]
# optional_silence.txt  [<phone>]

# Preparing language data
utils/prepare_lang.sh data/local/dict "<UNK>" data/local/lang data/lang
