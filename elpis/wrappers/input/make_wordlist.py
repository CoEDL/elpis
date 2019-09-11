#!/usr/bin/python3

"""
Given a json file with transcript information this tools can perform
manipulations including generating word lists.

Copyright: University of Queensland, 2019
Contributors:
              Josh Arnold - (The University of Queensland, 2017)
              Ben Foley - (The University of Queensland, 2018)
              Nicholas Lambourne - (The University of Queensland, 2019)
"""

import argparse
import os
import sys
from typing import List, Dict
from ..utilities import load_json_file


def save_word_list(word_list: List[str], file_name: str) -> None:
    """
    Given a list of strings, write them to a new file named filename.
    :param word_list: list of words to write.
    :param file_name: name of file to write word list to.
    """
    with open(file_name, "w", encoding='utf-8') as f:
        for word in word_list:
            f.write(word + "\n",)
        print(f"Wrote word list to {file_name}")


def extract_word_list(json_data: List[Dict[str, str]]) -> List[str]:
    """
    Unpack a dictionary constructed from a json_file - containing the key
    "transcript" - into a (Python) list of words.
    :param json_data: Python list of dictionaries read from a JSON file.
    :return: list of unique words from data, sorted alphabetically.
    """
    result: List[str] = []
    for utterance in json_data:
        words = utterance.get("transcript").split()
        result.extend(words)
    result = list(set(result))
    return sorted(result)


def extract_additional_words(file_name: str) -> List[str]:
    """
    Extracts words from an additional text file for the purpose
    of extending the lexicon to words that there is no sound data for.
    :param file_name: the name of the file to extract words from.
    :return: a list of words
    """
    words = []
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            print(f"Extracting additional words from {file_name}")
            for line in f.readlines():
                new_words = line.strip().split(" ")
                words += [word for word in new_words]
    else:
        print(f"WARNING: Additional word list file at {file_name} does not exist, skipping!")
    return words


def generate_word_list(transcription_file: str,
                       additional_word_list_file: str,
                       additional_corpus_file: str,
                       output_file: str) -> None:
    """
    Generates the wordlist.txt file used to populate the Kaldi file structure and generate
    the lexicon.txt file.
    :param transcription_file: path to the json file containing the transcriptions
    :param additional_word_list_file: file path to additional text wordlist
    :param additional_corpus_file: file path to the corpus.txt created
    :param output_file: the path of the file to write the word list to
    :return:
    """
    json_data: List[Dict[str, str]] = load_json_file(transcription_file)

    print("Extracting word list(s)...", flush=True, file=sys.stderr)

    # Retrieve ELAN word data
    word_list = extract_word_list(json_data)

    # Add additional words to lexicon if required
    if additional_word_list_file:
        additional_words = extract_additional_words(additional_word_list_file)
        word_list.extend(additional_words)

    if additional_corpus_file:
        corpus_file_words = extract_additional_words(additional_corpus_file)
        word_list.extend(corpus_file_words)

    # Remove duplicates
    word_list = list(set(word_list))

    print(sorted(word_list))

    print(f"Writing wordlist to file...", flush=True, file=sys.stderr)
    save_word_list(word_list, output_file)


def main():
    """
    Run the entire make_wordlist.py as a command line utility.

    Usage: python3 make_wordlist.py [-h] -i INFILE [-o OUTFILE] [-w WORDLIST] [-t TEXTCORPUS] [-c KALDICORPUS]
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile",
                        type=str,
                        required=True,
                        help="The json file containing the transcriptions.")
    parser.add_argument("-o", "--outfile",
                        type=str,
                        required=True,
                        help="The path of the file to write the word list to.")
    parser.add_argument("-w", "--word_list",
                        type=str,
                        required=False,
                        help="File path to an optional additional word list.")
    parser.add_argument("-c", "--kaldi_corpus",
                        type=str,
                        help="File path to the corpus.txt created by json_to_kaldi.py.",
                        required=True)
    arguments = parser.parse_args()

    generate_word_list(transcription_file=arguments.infile,
                       additional_word_list_file=arguments.word_list,
                       additional_corpus_file=arguments.kaldi_corpus,
                       output_file=arguments.outfile)

    print("Done.", file=sys.stderr)


if __name__ == '__main__':
    main()
