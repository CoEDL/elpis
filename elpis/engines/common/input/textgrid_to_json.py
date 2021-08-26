#!/usr/bin/python3

"""
Extracts transcription information from Praat (*.TextGrid) transcription files and outputs them
in json format

Copyright: University of Queensland, 2019
Contributors:
              Scott Heath - (University of Queensland, 2018)
              Nicholas Lambourne - (University of Queensland, 2019)
"""

import argparse
from praatio import tgio
from ..utilities import *


def process_textgrid(input_directory: str) -> List[Dict[str, Union[str, int]]]:
    """
    Traverses through the textgrid files in the given directory and extracts
    transcription information in each tier and creates a list of dictionaries,
    each containing data in the following format:
                        {'audio_file_name': <file_name>,
                        'transcript': <transcription_label>,
                        'start_ms': <start_time_in_milliseconds>,
                        'stop_ms': <stop_time_in_milliseconds>}

    :param input_directory: directory path containing input files from where the method
    :return: list of interval data in dictionary form
    """
    intervals: List[Dict[str, Union[str, int]]] = []

    for root, directories, files in os.walk(input_directory):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            if filename.endswith(".TextGrid"):
                textgrid: tgio.Textgrid = tgio.openTextgrid(os.path.join(root, filename))
                speech_tier: tgio.TextgridTier = textgrid.tierDict["Speech"]
                for start, stop, label in speech_tier.entryList:
                    label_word: str = label.replace('"', '')
                    intervals.append({
                        "audio_file_name": os.path.join(".", basename + ".wav"),
                        "transcript": label_word,
                        "start_ms": seconds_to_milliseconds(float(start)),
                        "stop_ms": seconds_to_milliseconds(float(stop))
                    })
    return intervals


def seconds_to_milliseconds(seconds: float) -> int:
    """
    Converts from seconds to milliseconds.

    :param seconds: time in seconds
    :return: converted time rounded to nearest millisecond
    """
    return int(seconds * 1000)


def main() -> None:

    """
    Run the entire textgrid_to_json.py as a command line utility.

    Usage: python3 textgrid_to_json.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR]
    """

    parser = argparse.ArgumentParser(
        description="Search input folder for .TextGrid files and convert to JSON on stdout")
    parser.add_argument("-i", "--input_dir", help="The input data dir", type=str, default="input/data/")
    parser.add_argument("-o", "--output_dir", help="Output directory", type=str, default="input/output/tmp")
    arguments = parser.parse_args()

    if not os.path.exists(arguments.output_dir):
        os.makedirs(arguments.output_dir)

    intervals = process_textgrid(arguments.input_dir)

    result_base_name, name = os.path.split(arguments.output_dir)
    if not name or name == ".":
        outfile_name = "intervals.json"
    else:
        outfile_name = os.path.join(name + ".json")

    output_json = os.path.join(result_base_name, outfile_name)
    write_data_to_json_file(data=intervals,
                            file_name=output_json)


if __name__ == "__main__":
    main()
