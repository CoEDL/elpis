#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

export PATH=$PATH:/kaldi/src/online2bin

echo "==== CTM output ===="

# Now, wav.scp needs to be in segment form
# eg audio_id filename
echo "decode audio.wav" > ./data/infer/split1/1/wav.scp

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

