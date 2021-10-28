#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

echo "==== Converting Textgrid to ELAN ===="
# python /kaldi-helpers/kaldi_helpers/output_scripts/textgrid_to_elan.py \
"${POETRY_PATH}/bin/python" /elpis/elpis/engines/common/output/textgrid_to_elan.py \
    --tg data/infer/utterance-0.TextGrid \
    --wav data/infer/wav.scp \
    --outfile data/infer/utterance-0.eaf
