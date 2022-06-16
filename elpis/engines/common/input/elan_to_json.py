#!/usr/bin/python3

"""
Get all files in the repository can use recursive atm as long as we don't need numpy
pass in corpus path throw an error if matching file wav isn't found in the corpus directory

Usage: python3 elan_to_json.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [-t TIER] [-j OUTPUT_JSON]

Copyright: University of Queensland, 2019
Contributors:
              Nicholas Lambourne - (The University of Queensland, 2018)
"""

import argparse
import glob
from loguru import logger
import os
import sys
from typing import List, Dict, Tuple, Optional

from pympi.Elan import Eaf
from ..utilities import load_json_file, write_data_to_json_file


def save_tier_info(
    input_eaf: Eaf = None,
    file_name: str = "",
    tier_types: Optional[List] = None,
    corpus_tiers_file: str = "corpus_tiers.json",
):
    tiers = []
    tier_types = tier_types or list()
    for tier_type in tier_types:
        tier_names = input_eaf.get_tier_ids_for_linguistic_type(tier_type)
        tiers.append({tier_type: tier_names})
    file_data = {"file": file_name, "tiers": tiers}
    corpus_tiers = load_json_file(corpus_tiers_file)
    corpus_tiers.append(file_data)
    write_data_to_json_file(data=corpus_tiers, file_name=corpus_tiers_file)


def process_eaf(
    input_elan_file: str = "",
    tier_order: int = 0,
    tier_type: str = "",
    tier_name: str = "",
    corpus_tiers_file: str = "",
) -> List[dict]:
    """
    Method to process a particular tier in an eaf file (ELAN Annotation Format).
    Transcriptions are read from an elan file tier.
    Tiers are nodes from the tree structure in the .eaf file.
    The tier to read from is determined by tier order (eg top tier would be order 1),
    tier type (eg default-lt) or tier name (eg Phrase).
    If tier type is used, the first tier matching this type is used.
    Elan can have multiple tiers of same type, future work would support reading data
    from multiple tiers of the selected type.

    It stores the transcriptions in the following format:
                    {'speaker_id': <speaker_id>,
                    'audio_file_name': <file_name>,
                    'transcript': <transcription_label>,
                    'start_ms': <start_time_in_milliseconds>,
                    'stop_ms': <stop_time_in_milliseconds>}

    :param input_elan_file: name of input elan file
    :param tier_order: index of the elan tier to process
    :param tier_type:  type of the elan tier to process
    :param tier_name:  name of the elan tier to process
    :param corpus_tiers_file list of all
    :return: a list of dictionaries, where each dictionary is an annotation
    """

    logger.info(f"processing eaf {input_elan_file} using {tier_order} {tier_type} {tier_name}")

    # Get paths to files
    input_directory, full_file_name = os.path.split(input_elan_file)
    file_name, extension = os.path.splitext(full_file_name)

    # Look for wav file matching the eaf file in same directory
    if os.path.isfile(os.path.join(input_directory, file_name + ".wav")):
        logger.info(f"WAV file found for {file_name}")
    else:
        raise ValueError(
            f"WAV file not found for {full_file_name}. "
            f"Please put it next to the eaf file in {input_directory}."
        )

    # Get tier data from Elan file
    input_eaf = Eaf(input_elan_file)
    tier_types: List[str] = list(input_eaf.get_linguistic_type_names())
    tier_names: List[str] = list(input_eaf.get_tier_names())

    # Keep this data handy for future corpus analysis
    save_tier_info(
        input_eaf=input_eaf,
        tier_types=tier_types,
        file_name=file_name,
        corpus_tiers_file=corpus_tiers_file,
    )

    # Get annotations and parameters (things like speaker id) on the target tier
    annotations: List[Tuple[str, str, str]] = []
    annotations_data: List[dict] = []

    # First try using tier order to get tier name
    if tier_order:
        # Watch out for files that may not have this many tiers
        # tier_order is 1-index but List indexing is 0-index
        try:
            tier_name = tier_names[tier_order - 1]
            logger.info(f"using tier order {tier_order} to get tier name {tier_name}")
        except IndexError:
            logger.warning("couldn't find a tier")
            pass
    else:
        # else use tier type to get a tier name
        if tier_type in tier_types:
            logger.info(f"found tier type {tier_type}")
            tier_names = input_eaf.get_tier_ids_for_linguistic_type(tier_type)
            tier_name = tier_names[0]
            if tier_name:
                logger.info(f"found tier name {tier_name}")
        else:
            logger.warning("tier type not found in this file")

    if tier_name in tier_names:
        logger.info(f"using tier name {tier_name}")
        annotations = input_eaf.get_annotation_data_for_tier(tier_name)

    if annotations:
        logger.info(f"annotations {annotations}")
        annotations = sorted(annotations)
        parameters: Dict[str, str] = input_eaf.get_parameters_for_tier(tier_name)
        logger.info(f"parameters {parameters}")
        speaker_id: str = parameters.get("PARTICIPANT", "")

    for annotation in annotations:
        start: str = annotation[0]
        end: str = annotation[1]
        annotation_text: str = annotation[2]

        logger.info(f"annotation {annotation} {start} {end}")
        obj = {
            "audio_file_name": f"{file_name}.wav",
            "transcript": annotation_text,
            "start_ms": start,
            "stop_ms": end,
        }
        if "PARTICIPANT" in parameters:
            obj["speaker_id"] = speaker_id
        annotations_data.append(obj)

    return annotations_data


def main():
    """
    Run the entire elan_to_json.py as a command line utility. It extracts information on speaker, audio file,
    transcription etc. from the given tier of the specified .eaf file.

    Usage: python3 elan_to_json.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [-t TIER] [-j OUTPUT_JSON]
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="This script takes an directory with ELAN files and "
        "slices the audio and output text in a format ready "
        "for our Kaldi pipeline."
    )
    parser.add_argument(
        "-i",
        "--input_dir",
        help="Directory of dirty audio and eaf files",
        default="working_dir/input/data/",
    )
    parser.add_argument(
        "-o", "--output_dir", help="Output directory", default="../input/output/tmp/"
    )
    parser.add_argument("-t", "--tier", help="Target language tier name", default="Phrase")
    parser.add_argument("-j", "--output_json", help="File path to output json")
    arguments: argparse.Namespace = parser.parse_args()

    # Build output directory if needed
    if not os.path.exists(arguments.output_dir):
        os.makedirs(arguments.output_dir)

    all_files_in_directory = set(glob.glob(os.path.join(arguments.input_dir, "**"), recursive=True))
    input_elan_files = [file_ for file_ in all_files_in_directory if file_.endswith(".eaf")]

    annotations_data = []

    for input_elan_file in input_elan_files:
        annotations_data.extend(
            process_eaf(input_elan_file=input_elan_file, tier_name=arguments.tier)
        )

    write_data_to_json_file(data=annotations_data, file_name=arguments.output_json)


if __name__ == "__main__":
    main()
