#!/bin/bash

# Copyright: University of Queensland, 2019
# Contributors:
#               Ben Foley (University of Queensland, 2018)

# prepare files needed for infer-align script
# this expects test-train to have been run
# single audio file only for now..

# Rename the audio file to conform to expectations
#
# mv working_dir/input/infer/*.wav working_dir/input/infer/audio.wav

# make ids

rec_id="decode"

spk_id=$(head -n 1 working_dir/input/output/kaldi/data/test/spk2utt | awk '{print $1}')

utt_id="$spk_id-utterance0"

start_ms=0

stop_ms=$(sox working_dir/input/infer/audio.wav -n stat 2>&1 | sed -n 's#^Length (seconds):[^0-9]*\([0-9.]*\)$#\1#p')




# write files

# spk2utt
# <speaker_id> <utterance_id>
# New line is added by default

echo -e "$spk_id $utt_id" > working_dir/input/infer/spk2utt

# utt2spk
# Same as above, but in reverse.

echo -e "$utt_id $spk_id" > working_dir/input/infer/utt2spk

echo -e "$utt_id $rec_id $start_ms $stop_ms" > working_dir/input/infer/segments

# wav.scp
# Format is <recording_id> <path/to/audio.file>

echo -e "decode data/infer/audio.wav" > working_dir/input/infer/wav.scp


# Clear out previous infer data in Kaldi

# rm -rf working_dir/input/infer/results working_dir/input/output/kaldi/data/infer

rm -rf working_dir/input/infer/results working_dir/input/output/kaldi/data/infer

