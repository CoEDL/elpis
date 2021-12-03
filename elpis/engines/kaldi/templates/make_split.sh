# Assuming we are decoding a single utterance still

# Manipulate the wav.scp file in the first (and only) split
line=$(head -n 1 ./data/infer/spk2utt)
utt=` echo ${line} | cut -d ' ' -f 2`
spk=` echo ${line} | cut -d ' ' -f 1` # this was seg

audio=$(<./data/infer/audio_meta.txt)
length=`sox --i -D ${audio}`
recid="decode"

# Prepare the split dir
splitDir=./data/infer/split1/
if [[ -d $splitDir ]]; then rm -r $splitDir; fi
mkdir -p "$splitDir/1"

# Argh.. the wav.scp file here should be in {utterance_id} to {audio_file} form
# unlike other usage which requires {audio_id} to {audio_file} format
# (such as below when we convert ctm to textgrid)
echo "${utt} ${audio}" > ./data/infer/split1/1/wav.scp
echo "${utt} ${spk}" > ./data/infer/split1/1/utt2spk
echo "${spk} ${utt}" > ./data/infer/split1/1/spk2utt
echo "${utt} ${recid} 0.00 ${length}" > ./data/infer/split1/1/segments

