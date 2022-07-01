import json

from typing import Dict, List

from flask import request, make_response
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.pron_dict import PronDict
from elpis.engines.common.errors import InterfaceError
from elpis.engines.common.input import extract_sound_mappings
from .utils.wrappers import file_param, require_dataset, require_pron_dict
from .utils.statistics import (
    parse_grapheme_frequency_from_dataset,
    get_length_of_wav,
    generate_word_sankey,
    generate_grapheme_sankey,
)
from elpis.engines.common.utilities import load_json_file

bp = Blueprint("statistics", __name__, url_prefix="/statistics")


@bp.route("/frequency/word", methods=["GET"])
@require_dataset
@file_param
def frequency(dataset: Dataset, file_name: str = None):
    """
    Returns the frequency of all words in a dataset, also known
    as the wordlist file.
    When specified with a file, returns the frequency of words for that specific file.
    """
    data = {}
    if file_name is not None:
        annotations: List[Dict[str, str]] = load_json_file(
            f"{dataset.pathto.annotation_json}"
        )
        frequency = {}
        for transcription in annotations:
            if transcription["audio_file_name"] == (file_name + ".wav"):
                words = transcription["transcript"].split()
                for word in words:
                    frequency[word] = frequency.get(word, 0) + 1
        data = frequency
    else:
        frequency = ""
        with dataset.pathto.word_count_json.open() as f:
            frequency = json.load(f)
        data = frequency
    return jsonify({"status": 200, "data": data})


@bp.route("/frequency/graphemes")
@require_dataset
@require_pron_dict
@file_param
def graphemes(pron_dict: PronDict, dataset: Dataset, file_name: str = None):
    """
    Returns the frequency of graphemes in the dataset, or for the specified file.
    """
    annotations: List[Dict[str, str]] = load_json_file(
        f"{dataset.pathto.annotation_json}"
    )
    graphemes = [text for (text, _) in extract_sound_mappings(pron_dict.l2s_path)]
    phrases = []
    if file_name is not None:
        phrases = [
            annotation["transcript"]
            for annotation in annotations
            if annotation["audio_file_name"] == file_name + ".wav"
        ]
    else:
        phrases = [annotation["transcript"] for annotation in annotations]
    if graphemes == False:
        return jsonify(
            {
                "status": 404,
                "data": "No current letter 2 sound exists (perhaps create one first)",
            }
        )
    return jsonify(
        {
            "status": 200,
            "data": parse_grapheme_frequency_from_dataset(phrases, graphemes),
        }
    )


@bp.route("/count", methods=["GET"])
@require_dataset
@file_param
def count(dataset: Dataset, file_name: str = None):
    """
    Returns the count of words for the dataset, or for the specified file.
    """
    transcriptions = []
    if file_name is not None:
        transcriptions = [
            t
            for t in load_json_file(f"{dataset.pathto.annotation_json}")
            if t["audio_file_name"] == (file_name + ".wav")
        ]
    else:
        transcriptions = load_json_file(f"{dataset.pathto.annotation_json}")
    count = 0
    for transcription in transcriptions:
        count += len(transcription["transcript"].split())
    return jsonify({"status": 200, "data": count})


@bp.route("/annotated")
@require_dataset
@file_param
def annotated(dataset: Dataset, file_name: str = None):
    """
    Returns the ratio of annotated to un-annotated for the dataset, or for the specified file.
    """
    annotations: List[Dict[str, str]] = load_json_file(
        f"{dataset.pathto.annotation_json}"
    )
    annotated_time, total_time = 0, 0
    if file_name is not None:
        total_time = get_length_of_wav(
            dataset.pathto.original.joinpath(file_name + ".wav")
        )
        for transcription in annotations:
            if transcription["audio_file_name"] == (file_name + ".wav"):
                annotated_time += transcription["stop_ms"] - transcription["start_ms"]
        return jsonify(
            {"status": 200, "annotated": annotated_time / float(total_time * 1000)}
        )
    else:
        for file_name in [f for f in dataset.files if f.endswith(".wav")]:
            total_time += get_length_of_wav(dataset.pathto.original.joinpath(file_name))
        for transcription in annotations:
            annotated_time += transcription["stop_ms"] - transcription["start_ms"]
    return jsonify(
        {
            "status": 200,
            "data": {"annotated": annotated_time / float(total_time * 1000)},
        }
    )


@bp.route("/sankey/word")
@require_dataset
@file_param
def sankey_word(dataset: Dataset, file_name: str = None):
    """
    Returns an object that can used to generate a sankey graph that shows order of words in the dataset.
    """
    annotations: List[Dict[str, str]] = load_json_file(
        f"{dataset.pathto.annotation_json}"
    )
    phrases = []
    if file_name is not None:
        phrases = [
            annotation["transcript"]
            for annotation in annotations
            if annotation["audio_file_name"] == file_name + ".wav"
        ]
    else:
        phrases = [annotation["transcript"] for annotation in annotations]
    return jsonify({"status": 200, "data": {"sankey": generate_word_sankey(phrases)}})


@bp.route("/sankey/grapheme")
@require_dataset
@require_pron_dict
@file_param
def sankey_grapheme(pron_dict: PronDict, dataset: Dataset, file_name: str = None):
    """
    Returns an object that can used to generate a sankey graph that shows order of graphemes in the dataset.
    """
    annotations: List[Dict[str, str]] = load_json_file(
        f"{dataset.pathto.annotation_json}"
    )
    graphemes = [text for (text, _) in extract_sound_mappings(pron_dict.l2s_path)]
    phrases = []
    if file_name is not None:
        phrases = [
            annotation["transcript"]
            for annotation in annotations
            if annotation["audio_file_name"] == file_name + ".wav"
        ]
    else:
        phrases = [annotation["transcript"] for annotation in annotations]
    return jsonify(
        {
            "status": 200,
            "data": {"sankey": generate_grapheme_sankey(phrases, graphemes)},
        }
    )


@bp.route("/swarmplot/files")
@require_dataset
def swarm_plot_files(dataset: Dataset):
    """
    Returns an object that provides a swarmplot overview of a dataset.
    The position being the length of the audio file
    The size being the count of words in the file
    """
    annotations: List[Dict[str, str]] = load_json_file(
        f"{dataset.pathto.annotation_json}"
    )
    swarm_plot = {}
    id_counter = 0
    for annotation in annotations:
        file_name = annotation["audio_file_name"]
        if file_name.endswith(".wav"):
            file_name = file_name[:-4]
        else:
            # TODO(jack) error in this case, invalid state
            pass
        if file_name not in swarm_plot:
            swarm_plot[file_name] = {
                "file": file_name,
                "group": "Files",
                "length": get_length_of_wav(
                    dataset.pathto.original.joinpath(annotation["audio_file_name"])
                ),
                "count": len(annotation["transcript"].split(" ")),
                "annotated": annotation["stop_ms"] - annotation["start_ms"],
            }
            id_counter += 1
        else:
            swarm_plot[file_name]["count"] += len(annotation["transcript"].split(" "))
            swarm_plot[file_name]["annotated"] += (
                annotation["stop_ms"] - annotation["start_ms"]
            )
    # Transform annotated values now that we know the total length and total annotated length
    for val in swarm_plot.values():
        print((val["annotated"], val["length"]))
        val["annotated"] = val["annotated"] / float(val["length"]) / float(1000)

    counts = [val["count"] for val in swarm_plot.values()]
    min_count, max_count = min(counts), max(counts)

    return jsonify({"status": 200, "data": {"swarmplot": list(swarm_plot.values())}})
