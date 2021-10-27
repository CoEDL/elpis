#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

# Now, wav.scp needs to be in segment form
# eg audio_id filename
echo "decode audio.wav" > ./data/infer/split1/1/wav.scp

echo "==== Converting CTM to Textgrid ===="
# python /kaldi-helpers/kaldi_helpers/output_scripts/ctm_to_textgrid.py \
"${POETRY_PATH}/bin/python" /elpis/elpis/engines/common/output/ctm_to_textgrid.py \
    --ctm data/infer/align-words-best-wordkeys.ctm \
    --wav data/infer/split1/1/wav.scp \
    --seg data/infer/split1/1/segments \
    --outdir data/infer
