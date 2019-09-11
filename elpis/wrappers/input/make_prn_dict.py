#!/usr/bin/python3

"""
This is script automatically builds a pronunciation (word->sounds) dictionary

Copyright: University of Queensland, 2019
Contributors:

"""

import argparse
import sys
from typing import List, Tuple, Set, TextIO


def extract_words(input_file_name: str) -> List[str]:
    """
    Extracts a list of words from a word list. Expects one word per line.
    :param input_file_name: the path of the file to extract the words from
    :return: a list of words
    """
    input_tokens = []
    with open(input_file_name, "r", encoding='utf-8') as input_file:
        for line in input_file.readlines():
            token = line.strip()
            if len(token) > 0:
                input_tokens.append(token)
    return input_tokens


def extract_sound_mappings(config_file_name: str) -> List[Tuple[str, str]]:
    """
    Extract a list of mappings from characters/symbols to sounds.
    :param config_file_name: the path to the file to extract the mappings from
    :return: a list of tuples consisting containing (symbol, sound_equivalent)
    """
    sound_mappings = []
    with open(config_file_name, "r", encoding='utf-8') as config_file:
        for line in config_file.readlines():
            if line[0] == '#':
                continue

            mapping = list(filter(None, line.strip().split(' ', 1)))

            if len(mapping) > 1:
                sound_mappings.append((mapping[0], mapping[1]))
    return sound_mappings


def generate_sound_mapping(word: str,
                           sound_map: List[Tuple[str, str]],
                           output_file: TextIO,
                           missing_characters: Set[str]) -> None:
    """
    Writes the pronunciation mapping for a particular word to the given output file.
    :param word: the word to generate a pronunciation mapping for
    :param sound_map: the sound map to base the pronunciation on
    :param output_file: the file to write the mapping to
    :param missing_characters: a list to store any unrecognised characters in
    """
    current_index = 0
    res = [word]
    token_lower = word.lower()

    while current_index < len(token_lower):
        found = False
        for maps in sound_map:
            if token_lower.find(maps[0], current_index) == current_index:
                found = True
                res.append(maps[1])
                current_index += len(maps[0])
                break

        if not found:
            # unknown sound
            res.append('(' + token_lower[current_index] + ')')
            missing_characters.add(token_lower[current_index])
            current_index += 1

    output_file.write(' '.join(res) + '\n')


def generate_pronunciation_dictionary(word_list: str,
                                      pronunciation_dictionary: str,
                                      config_file: str) -> None:
    """
    Creates a dictionary of pronunciations based on the provided word list and sound rules.
    :param word_list: the file path to the list of words to add to the pronunciation dictionary
    :param pronunciation_dictionary: the path to the file to write the pronunciation dictionary
    :param config_file: the path to the file with the symbol -> sound mapping
    """
    words = extract_words(word_list)
    sound_map = extract_sound_mappings(config_file)
    sound_map.sort(key=lambda x: len(x[0]), reverse=True)  # Sort by length of sound map

    missing_characters = set()

    with open(pronunciation_dictionary, "w", encoding='utf-8') as output_file:
        output_file.write('!SIL sil\n')
        output_file.write('<UNK> spn\n')
        for word in words:
            generate_sound_mapping(word=word,
                                   sound_map=sound_map,
                                   output_file=output_file,
                                   missing_characters=missing_characters)

    for character in missing_characters:
        print(f"Unexpected character: {character}", file=sys.stderr)

    print(f"Wrote lexicon to {pronunciation_dictionary}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile",
                        type=str,
                        required=True,
                        help="")
    parser.add_argument("-o", "--outfile",
                        type=str,
                        required=True,
                        help="name of the output file")
    parser.add_argument("-c", "--config",
                        type=str,
                        required=True,
                        help="configuration file with one letter/symbol -> sound mapping in each line")
    arguments = parser.parse_args()

    generate_pronunciation_dictionary(word_list=arguments.infile,
                                      pronunciation_dictionary=arguments.outfile,
                                      config_file=arguments.config)


if __name__ == "__main__":
    main()
