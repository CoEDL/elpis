#!/bin/bash

# Get run command (which logs) from script file
. ./cmd.sh
# Put typical Kaldi binaries onto the path
. ./path.sh

# build the Elan file
"${POETRY_PATH}/bin/python" /elpis/elpis/engines/common/output/ctm_to_elan.py \
    --ctm data/infer/ctm_with_conf.ctm \
    --wav data/infer/split1/1/wav.scp \
    --seg data/infer/split1/1/segments \
    --outdir data/infer \
    --confidence
