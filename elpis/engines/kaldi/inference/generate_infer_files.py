"""
Generates files requires to do infer with untranscribed audio.
Files need trailing newline, otherwise Kaldi fails silently.
NB: Single-file only for now, it doesn't handle multiple files.

- spk2utt
    <speaker_id> <utterance_id>
    This file lists an ID for the speaker and an id for the utterance,
    space separated.
    We're getting the speaker id from one of the test files,
    which isn't ideal especially in multi-speaker corpora.
    TODO: add an interface that selects the speaker

- utt2spk
    <utterance_id> <speaker_id>
    Same as above but in reverse

- segments
    <utt_id> <rec_id> <start_ms> <stop_ms>
    This lists start and stop times of the segments.
    For single, short audio it should be just the duration of the file

- wav.scp
    <recording_id> <path/to/audio.file>
    This assocaites the recording ID used above to the audio filename
"""

from pathlib import Path
import os
import wave
import contextlib


# echo -e "$spk_id $utt_id" > working_dir/input/infer/spk2utt
def build_spk2utt_file(path, spk_id, utt_id):
    spk2utt_path = Path(path).joinpath('spk2utt')
    with spk2utt_path.open(mode='w') as fout:
        fout.write(f'{spk_id} {utt_id}\n')


# echo -e "$utt_id $spk_id" > working_dir/input/infer/utt2spk
def build_utt2spk_file(path, utt_id, spk_id):
    utt2spk_path = Path(path).joinpath('utt2spk')
    with utt2spk_path.open(mode='w') as fout:
        fout.write(f'{utt_id} {spk_id}\n')


# echo -e "$utt_id $rec_id $start_ms $stop_ms" > working_dir/input/infer/segments
def build_segments_file(path, utt_id, rec_id, start_ms, stop_ms):
    segments_path = Path(path).joinpath('segments')
    with segments_path.open(mode='w') as fout:
        fout.write(f'{utt_id} {rec_id} {start_ms} {stop_ms}\n')


# echo -e "decode data/infer/audio.wav" > working_dir/input/infer/wav.scp
def build_wav_scp_file(path, rec_id, rel_audio_file_path):
    wav_scp_path = Path(path).joinpath('wav.scp')
    with wav_scp_path.open(mode='w') as fout:
        fout.write(f'{rec_id} {rel_audio_file_path}\n')


# Prepare the values we need
def generate_files(transcription):
    # This is our transcription directory (state object directory)
    path = transcription.path

    # Expecting filename to be audio.wav. TODO support accepting any name
    audio_file_name = 'audio.wav'

    # Get the speaker id from the model > kaldi/data/test/spk2utt file. it's the first "word".
    # spk_id=$(head -n 1 working_dir/input/output/kaldi/data/test/spk2utt | awk '{print $1}')
    model_spk2utt_path = Path(transcription.model.path).joinpath('kaldi/data/test/spk2utt')
    with model_spk2utt_path.open(mode='r') as fin:
        spk_id = fin.read().split()[0]

    # Arbitrary id for each utterance. assuming one utterance for now
    utt_id = spk_id + '-utterance0'

    # Expecting to start at 0 time. Could benefit from VAD here?
    start_ms = 0

    # Duration of the audio
    # stop_ms=$(sox working_dir/input/infer/audio.wav -n stat 2>&1 |
    # sed -n 's#^Length (seconds):[^0-9]*\([0-9.]*\)$#\1#p')
    abs_audio_file_path = Path(path).joinpath(audio_file_name)
    with contextlib.closing(wave.open(str(abs_audio_file_path), 'r')) as fin:
        frames = fin.getnframes()
        rate = fin.getframerate()
        stop_ms = frames / float(rate)

    # Rec id is arbitrary, use anything you like here
    rec_id = 'decode'

    # Path to the audio, relative to kaldi working dir
    rel_audio_file_path = os.path.join('data', 'infer', audio_file_name)

    # Generate the files
    build_spk2utt_file(path, spk_id, utt_id)
    build_utt2spk_file(path, utt_id, spk_id)
    build_segments_file(path, utt_id, rec_id, start_ms, stop_ms)
    build_wav_scp_file(path, rec_id, rel_audio_file_path)
    print("done generate_files")
