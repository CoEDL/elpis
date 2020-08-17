#!/bin/bash

. ./path.sh || exit 1
. ./cmd.sh || exit 1

nj=1       # number of parallel jobs - 1 is perfect for such a small data set
lm_order=1 # language model order (n-gram quantity) - 1 is enough for digits grammar

echo
echo "===== LANGUAGE MODEL CREATION ====="
echo "===== MAKING lm.arpa ====="
echo

loc=`which ngram-count`;
if [ -z $loc ]; then
   if uname -a | grep 64 >/dev/null; then
        sdir=$KALDI_ROOT/tools/srilm/bin/i686-m64
   else
        sdir=$KALDI_ROOT/tools/srilm/bin/i686
   fi
   if [ -f $sdir/ngram-count ]; then
        echo "Using SRILM language modelling tool from $sdir"
        export PATH=$PATH:$sdir
   else
        echo "SRILM toolkit is probably not installed.
                Instructions: tools/install_srilm.sh"
        exit 1
   fi
fi

local=data/local
mkdir $local/tmp
ngram-count -order $lm_order -write-vocab $local/tmp/vocab-full.txt -wbdiscount -text $local/corpus.txt -lm $local/tmp/lm.arpa

echo
echo "===== MAKING G.fst ====="
echo

lang=data/lang
arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang/words.txt $local/tmp/lm.arpa $lang/G.fst
