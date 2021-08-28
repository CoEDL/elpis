#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

# Activate Python 3.8.2 virtual environment
source /venv/bin/activate

# Manipulate the wav.scp file in the first (and only) split
line=$(head -n 1 ./data/infer/spk2utt)
utt=` echo ${line} | cut -d ' ' -f 2`
spk=` echo ${line} | cut -d ' ' -f 1` # this was seg
audio="audio.wav"
length=`sox --i -D ${audio}`
recid="decode"

# Now, wav.scp needs to be in segment form
# eg audio_id filename
echo "${recid} ${audio}" > ./data/infer/split1/1/wav.scp

echo "==== Converting CTM to Textgrid ===="
# python /kaldi-helpers/kaldi_helpers/output_scripts/ctm_to_textgrid.py \
"{POETRY_PATH}/bin/python" /elpis/elpis/engines/common/output/ctm_to_textgrid.py \
    --ctm data/infer/align-words-best-wordkeys.ctm \
    --wav data/infer/split1/1/wav.scp \
    --seg data/infer/split1/1/segments \
    --outdir data/infer
