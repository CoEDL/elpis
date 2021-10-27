#!/usr/bin/python3

"""
Takes a CTM (time aligned) file and produces an Elan file.
If the CTM has confidence values, write them as a ref tier.

Copyright: University of Queensland, 2021
Contributors:
             Ben Foley - (University of Queensland, 2021)
             Nicholas Lambourne - (University of Queensland, 2018)
"""

from argparse import ArgumentParser
from csv import reader
from pathlib import Path
from typing import Dict, Tuple
import codecs
from pympi.Elan import Eaf


def ctm_to_dictionary(ctm_file_path: str,
                      segments_dictionary: Dict[str, str],
                      confidence: bool) -> dict:
    with codecs.open(ctm_file_path, encoding="utf8") as file:
        ctm_entries = list(reader(file, delimiter=" "))
    ctm_dictionary = dict()
    for entry in ctm_entries:
        utterance_id, segment_start_time = segments_dictionary[entry[0]]
        if utterance_id not in ctm_dictionary:
            ctm_dictionary[utterance_id] = []
        relative_start_time = float(entry[2])
        absolute_start_time = segment_start_time + relative_start_time
        absolute_end_time = absolute_start_time + float(entry[3])
        inferred_text = entry[4]
        confidence = entry[5] if confidence else None
        utterance_segment = (str(absolute_start_time),
                             str(absolute_end_time),
                             inferred_text,
                             confidence)
        ctm_dictionary[utterance_id].append(utterance_segment)
    return ctm_dictionary

def get_segment_dictionary(segment_file_name: str) -> Dict[str, Tuple[str, float]]:
    with open(segment_file_name, "r") as file:
        segment_entries = list(reader(file, delimiter=" "))
    segment_dictionary = dict()
    for entry in segment_entries:
        segment_id = entry[0]
        utterance_id = entry[1]
        start_time = float(entry[2])
        segment_dictionary[segment_id] = (utterance_id, start_time)
    return segment_dictionary

def wav_scp_to_dictionary(scp_file_name: str) -> dict:
    wav_dictionary = dict()
    with open(scp_file_name) as file:
        wav_entries = list(reader(file, delimiter=" "))
        for entry in wav_entries:
            utterance_id = entry[0]
            wav_file_path = entry[1]
            wav_dictionary[utterance_id] = wav_file_path
    return wav_dictionary

def create_eaf_and_textgrid(wav_dictionary:dict,
               ctm_dictionary:dict,
               confidence:bool,
               output_directory:str):
    for index, [utterance_id, basename] in enumerate(wav_dictionary.items()):
        eaf = Eaf()
        eaf.add_linked_file(str(Path(output_directory, basename)))
        eaf.add_linguistic_type("conf_lt", "Symbolic_Association")
        eaf.add_tier("default")
        if confidence:
            eaf.add_tier("confidence", parent="default", ling="conf_lt")
        for annotation in ctm_dictionary[utterance_id]:
            # Annotation looks like ('0.32', '0.52', 'word', '0.81')
            # Convert times to ms integers
            start, end, value, *conf = annotation
            start_ms = int(float(start) * 1000)
            end_ms = int(float(end) * 1000)
            # Add the transcription annotation
            eaf.add_annotation("default", start_ms, end_ms, value)
            # Add the confidence value as a reference annotation
            if conf:
                # Add a time value to the start time so the ref falls within a parent slot
                eaf.add_ref_annotation("confidence", "default", start_ms+1, conf[0])

        # Save as Elan eaf file
        output_eaf = str(Path(output_directory, f'utterance-{index}.eaf'))
        eaf.to_file(output_eaf)

        # Make a Textgrid format version
        output_textgrid = str(Path(output_directory, f'utterance-{index}.Textgrid'))
        textgrid = eaf.to_textgrid()
        textgrid.to_file(output_textgrid)


def main() -> None:
    parser: ArgumentParser = ArgumentParser(description="Converts Kaldi CTM format to Elan .eaf format.")
    parser.add_argument("-c", "--ctm",
                        type=str,
                        help="The input CTM format file",
                        required=True)
    parser.add_argument("-w", "--wav",
                        type=str,
                        help="The input wav.scp file",
                        required=True)
    parser.add_argument("-s", "--seg",
                        type=str,
                        help="The segment to utterance mapping",
                        default="./segments")
    parser.add_argument("-o", "--outdir",
                        type=str,
                        help="The directory path for the Elan output",
                        default=".")
    parser.add_argument('--confidence', dest='confidence', action='store_true')
    parser.add_argument('--no-confidence', dest='confidence', action='store_false')
    parser.set_defaults(confidence=True)

    arguments = parser.parse_args()

    segments_dictionary = get_segment_dictionary(arguments.seg)
    ctm_dictionary = ctm_to_dictionary(arguments.ctm, segments_dictionary, arguments.confidence)
    wav_dictionary = wav_scp_to_dictionary(arguments.wav)
    output_directory = Path(arguments.outdir)

    if not output_directory.parent:
        Path.mkdir(output_directory.parent, parents=True)

    create_eaf_and_textgrid(wav_dictionary,
                            ctm_dictionary,
                            arguments.confidence,
                            output_directory)

if __name__ == '__main__':
    main()
