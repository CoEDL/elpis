#!/bin/bash

# Copyright: University of Queensland, 2019
# Contributors:
#               Nicholas Lambourne - (University of Queensland, 2019)

# USAGE:
#    $ task _infer-align
#
#    N.B: relies on the go-task task runner and related Taskfile.yml
#
#    This script is meant to demonstrate how an already trained GMM-HMM
#    model and its corresponding HCLG graph, built via Kaldi,
#    can be used to decode new audio files.
#
#    It relies on a model already being prepared, which you can achieve
#    via `task _run-elan` followed by `task _train-test`
#

# INPUT:
#    data/
#       infer/          <= currently copied from test data
#           wav.scp
#           utt2spk
#           spk2utt
#           segments
#           ...
#
#    config/            <= created when triphone model is trained
#        mfcc.conf
#
#    exp/
#        tri/
#            final.mdl  <= all copied verbatim from pre-trained triphone model
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
#            1best-fst.tra
#            1best-fst-word-aligned.tra
#            align-words-best-wordkeys.ctm
#            utterance-0.TextGrid
#            utterance-0.eaf



. ./path.sh
# make sure you include the path to the gmm bin(s)
# the following two export commands are what my path.sh script contains:
# export PATH=$PWD/utils/:$PWD/../../../src/bin:$PWD/../../../tools/openfst/bin:$PWD/../../../src/fstbin/:$PWD/../../../src/gmmbin/:$PWD/../../../src/featbin/:$PWD/../../../src/lm/:$PWD/../../../src/sgmmbin/:$PWD/../../../src/fgmmbin/:$PWD/../../../src/latbin/:$PWD/../../../src/nnet2bin/:$PWD:$PATH
# export LC_ALL=C

# CREATE REQUIRED DIRECTORIES
# mkdir ./data/infer

# COPY TRAINED MODEL
echo "==== Copying Pretrained Model ===="
cp -R ./exp/tri1 ./exp/tri
# cp ./data/test/* ./data/infer
# rm ./data/infer/text

# CREATE MFCC (mel-frequency cepstral coefficients)
# args:
#      nj: number of parallel jobs
#      data directory:
#      mfcc directory: the directory in which to put the MFCC
#
echo "==== Creating Mel-Frequency Cepstral Coefficients (MFCCs) ===="
steps/make_mfcc.sh --nj 1 \
    data/infer exp/make_mfcc/infer \
    mfcc

# MFCC + DELTAS --> FEATURE VECTORS
# args:
#       --utt2spk: utterance to speaker mapping
#       trained CMVN: cepstral mean and variance normalisation
#       trained MFCC: mel-frequency cepstral coefficients
#       PIPED INTO add-deltas (adds delta features)
#       args:
#             delta features
echo "==== Extracting Feature Vectors ===="
apply-cmvn --utt2spk=ark:data/infer/utt2spk \
    scp:mfcc/cmvn_test.scp \
    scp:mfcc/raw_mfcc_infer.1.scp ark:- | \
    add-deltas ark:- ark:data/infer/delta-feats.ark

# TRAINED GMM-HMM + FEATURE VECTORS --> LATTICE
# args:
#       -- word symbol table input file specifier
#       model input file specifier
#       FST input file specifier
#       feature input file specifier
#       lattice output file specifier
echo "==== Creating Lattice ===="
gmm-latgen-faster \
    --word-symbol-table=exp/tri/graph/words.txt \
    exp/tri/final.mdl \
    exp/tri/graph/HCLG.fst \
    ark:data/infer/delta-feats.ark \
    ark,t:data/infer/lattices.ark

# LATTICE --> BEST PATH THROUGH LATTICE AS FST (Finite State Transducer)
# args:
#       input lattice file specifier
#       output lattice (FST format) file specifier
echo "==== Finding Best Path (Transcription) ===="
lattice-1best \
    ark:data/infer/lattices.ark \
    ark,t:data/infer/1best-fst.tra

# LATTICE-FST --> LATTICE WITH WORD BOUNDARIES
# args:
#       word boundaries file specifier
#       model input file specifier
#       FST lattice input file specifier
#       lattice output file specifier
echo "==== Adding Word Boundaries to FST ===="
lattice-align-words \
    data/lang/phones/word_boundary.int \
    exp/tri/final.mdl \
    ark,t:data/infer/1best-fst.tra \
    ark,t:data/infer/1best-fst-word-aligned.tra

# LATTICE WITH WORD BOUNDARIES --> CTM FORMAT (INT-WORDS)
# args:
#       aligned linear lattice input file specifier
#       ctm (int) output file specifier
echo "==== Converting Lattice to CTM Format ===="
nbest-to-ctm \
    ark,t:data/infer/1best-fst-word-aligned.tra \
    data/infer/align-words-best-intkeys.ctm

# BEST PATH INTERGERS (CTM) --> BEST PATH WORDS (CTM)
# args:
#       mapping of integer keys to words
#       ctm file to change integers to words in
echo "==== Translating Word Indexes to Words ===="
utils/int2sym.pl -f 5- \
    exp/tri/graph/words.txt \
    data/infer/align-words-best-intkeys.ctm \
    > data/infer/align-words-best-wordkeys.ctm

./venv/bin/activate

# BEST PATH WORDS (CTM) --> TEXTGRID
echo "==== Converting CTM to Textgrid ===="
python /elpis/elpis/wrappers/output/ctm_to_textgrid.py \
    --ctm data/infer/align-words-best-wordkeys.ctm \
    --wav data/infer/wav.scp \
    --seg data/infer/segments \
    --outdir data/infer

# TEXTGRID --> ELAN
echo "==== Converting Textgrid to ELAN ===="
python /elpis/elpis/wrappers/output/textgrid_to_elan.py \
    --tg data/infer/utterance-0.TextGrid \
    --wav data/infer/wav.scp \
    --outfile data/infer/utterance-0.eaf

# REPORT OUTPUT (CTM is the only concise format)
echo "CTM output:"
cat ./data/infer/align-words-best-wordkeys.ctm
