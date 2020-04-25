#!/usr/bin/python3

"""
Parse json file and extract transcription information which are then processed and output in the desired Kaldi format.
The output files will be stored in two separate folders training and testing inside the specified output directory.

training :
    corpus.txt, text, segments, wav.scp, utt2spk, spk2utt
testing :
    corpus.txt, text, segments, wav.scp, utt2spk, spk2utt

The training folder is for the model creation using Kaldi, whereas the testing folder is used for verifying the
reliability of the model.

Copyright: University of Queensland, 2019
Contributors:
              Scott Heath - (University of Queensland, 2017)
              Nicholas Lambourne - (University of Queensland, 2019)
"""

import argparse
import json
import os
import uuid
from typing import Dict, List, TextIO


class KaldiInput:
    """
    Class to store information for the training and testing data sets.
    """

    def __init__(self, output_folder: str) -> None:

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        self.speakers: Dict[str, str] = {}
        self.recordings: Dict[str, str] = {}
        self.utterances: Dict[str, str] = {}

        self.segments_list: List[str] = []
        self.transcripts_list: List[str] = []
        self.speakers_list: List[str] = []
        self.recordings_list: List[str] = []
        self.utt2spk_list: List[str] = []
        self.corpus_list: List[str] = []

        self.segments_file: TextIO = open(f"{output_folder}/segments", "w", encoding="utf-8")
        self.transcripts_file: TextIO = open(f"{output_folder}/text", "w", encoding="utf-8")
        self.recordings_file: TextIO = open(f"{output_folder}/wav.scp", "w", encoding="utf-8")
        self.utt2spk_file: TextIO = open(f"{output_folder}/utt2spk", "w", encoding="utf-8")
        self.corpus_txt: TextIO = open(f"{output_folder}/corpus.txt", "w", encoding="utf-8")

    def add_speaker(self, speaker_id: str) -> str:
        """
        Adds a speaker element if it is not already present.

        :param speaker_id: speaker id - could be a name of a uuid code
        :return: returns the correctly formatted speaker id
        """
        if speaker_id not in self.speakers:
            self.speakers[speaker_id] = str(uuid.uuid4())  # create speaker id
            self.speakers_list.append(f"{self.speakers[speaker_id]} \n")  # writing gender # TODO Handle gender here
        return self.speakers[speaker_id]

    def add_recording(self, audio_file: str) -> str:
        """
        Adds an audio file it is not already present.

        :param audio_file: name of audio file
        :return: returns a correctly formatted audio file description
        """
        if audio_file not in self.recordings:
            self.recordings[audio_file] = str(uuid.uuid4())  # Create recording id
            self.recordings_list.append(f"{self.recordings[audio_file]} ./{audio_file}\n")
        return self.recordings[audio_file]

    def add(self, recording_id: str,
            speaker_id: str,
            utterance_id: str,
            start_ms: int,
            stop_ms: int,
            transcript: str,
            silence_markers: bool) -> None:
        """
        Appends new items to the transcripts, segments, utt2spk and corpus lists.

        :param recording_id: id for the recording file
        :param speaker_id: id for the speaker who uttered the phrase
        :param utterance_id: unique id for the uttered phrase
        :param start_ms: start of the uttered phrase
        :param stop_ms: stop time of the uttered phrase
        :param transcript: the uttered phrase
        :param silence_markers: boolean condition indicating whether to include silence markers
        """
        if silence_markers:
            self.transcripts_list.append(f"{utterance_id} !SIL {transcript} !SIL\n")
        else:
            self.transcripts_list.append(f"{utterance_id} {transcript} \n")
        self.segments_list.append(f"{utterance_id} {recording_id} {start_ms/1000.0} {stop_ms/1000.0}\n")
        self.utt2spk_list.append(f"{utterance_id} {speaker_id}\n")
        self.corpus_list.append(f"{transcript}\n")

    def write_and_close(self) -> None:
        """
        After parsing the json file and populating the segments, transcripts, speakers, recordings, utt2spk and corpus
        lists with data, this function performs the final write to their respective files.
        """

        self.segments_list.sort()
        self.segments_file.write("".join(self.segments_list))
        self.segments_file.close()

        self.transcripts_list.sort()
        self.transcripts_file.write("".join(self.transcripts_list))
        self.transcripts_file.close()

        self.recordings_list.sort()
        self.recordings_file.write("".join(self.recordings_list))
        self.recordings_file.close()

        self.utt2spk_list.sort()
        self.utt2spk_file.write("".join(self.utt2spk_list))
        self.utt2spk_file.close()

        self.corpus_list.sort()
        self.corpus_txt.write("".join(self.corpus_list))
        self.corpus_txt.close()


def extract_transcript(input_set: KaldiInput,
                       json_transcript: dict,
                       silence_markers: bool) -> None:
    """
    Extract a single transcript from json and add its contents to the given output set.
    :param input_set: the set to add the data from the transcript to (e.g. testing or training data)
    :param json_transcript:
    :param silence_markers: boolean condition indicating whether to include silence markers
    """
    transcript: str = json_transcript.get("transcript", "")
    start_ms: int = json_transcript.get("start_ms", 0)
    stop_ms: int = json_transcript.get("stop_ms", 0)

    # Speaker ID is not available in textgrid files
    if "speaker_id" in json_transcript:
        speaker_id: str = json_transcript.get("speaker_id", "")
    else:
        speaker_id: str = str(uuid.uuid4())

    audio_file: str = json_transcript.get("audio_file_name", "").replace("\\", "/")

    speaker_id = input_set.add_speaker(speaker_id)  # add speaker id
    recording_id: str = input_set.add_recording(audio_file)  # add audio file name
    utterance_id: str = speaker_id + "-" + str(uuid.uuid4())  # add utterance id
    input_set.add(recording_id,
                  speaker_id,
                  utterance_id,
                  start_ms,
                  stop_ms,
                  transcript,
                  silence_markers)


def create_kaldi_structure(input_json: str,
                           output_folder: str,
                           silence_markers: bool,
                           corpus_txt: str) -> None:
    """
    Create a full Kaldi input structure based upon a json list of transcriptions and an optional
    text corpus.
    :param input_json: the path to a json file with a list of transcriptions
    :param output_folder: the folder in which to create the kaldi file stucture
    :param silence_markers: boolean condition indicating whether to include silence markers
    :param corpus_txt: the path to the file to write all corpus examples to
    """
    testing_input = KaldiInput(output_folder=f"{output_folder}/testing")
    training_input = KaldiInput(output_folder=f"{output_folder}/training")

    try:
        with open(input_json, "r") as input_file:
            json_transcripts: str = json.loads(input_file.read())
    except FileNotFoundError:
        print(f"JSON file could not be found: {input_json}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, json_transcript in enumerate(json_transcripts):
        if i % 10 == 0:
            extract_transcript(input_set=testing_input,
                               json_transcript=json_transcript,
                               silence_markers=silence_markers)
        else:
            extract_transcript(input_set=training_input,
                               json_transcript=json_transcript,
                               silence_markers=silence_markers)

    if os.path.exists(corpus_txt):
        # Append the corpus text to the training data (it was cleaned in dataset step)
        with open(corpus_txt, "r") as file_:
            for line in file_.readlines():
                training_input.corpus_list.append(line)
    else:
        print("No additional text corpus provided.")

    testing_input.write_and_close()
    training_input.write_and_close()


def main() -> None:
    """
    Run the entire json_to_kaldi.py as a command line utility.

    Usage: python3 json_to_kaldi.py -i INPUT_JSON -o OUTPUT_FOLDER [-s] [-c CORPUS_TXT]
    """
    parser = argparse.ArgumentParser(description="Convert json from stdin to Kaldi input files "
                                                 "(in output-folder).")
    parser.add_argument("-i", "--input_json",
                        type=str,
                        help="The input json file",
                        required=True)
    parser.add_argument("-o", "--output_folder",
                        type=str,
                        help="The output folder",
                        default=os.path.join(".", "data"))
    parser.add_argument("-s", "--silence_markers",
                        action="store_true",
                        help="The input json file",
                        required=False)
    parser.add_argument("-c", "--corpus_txt",
                        type=str,
                        help="Path to the corpus.txt file to write text examples to",
                        required=False)
    arguments = parser.parse_args()

    create_kaldi_structure(input_json=arguments.input_json,
                           output_folder=arguments.output_folder,
                           silence_markers=arguments.silence_markers,
                           corpus_txt=arguments.corpus_txt)


if __name__ == "__main__":
    main()
