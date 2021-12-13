#!/usr/bin/python3

import librosa
from loguru import logger
import numpy
from typing import Any, Dict, List, Tuple

def get_chunks(audio_path: str, method: str, parameter: float) -> List[Tuple[float, float]]:
    """
    Chunk voice sections from audio data extracted from an audio path with the chosen method (with its parameter).

    :param audio_path: audio file path.
    :param method: chunking method (*duration*, *offset* or *threshold*).
    :param parameter: parameter of the chosen method.
    :return: a list of tuples of voice sections (timestamps of start and end).
    """
    audio_data = read_audio_path(audio_path)
    threshold = find_best_threshold(audio_data, method=method, parameter=parameter)
    logger.info(f"Top db = {audio_data['top db']}, chosen threshold = {threshold} (method = {method})")
    time_voice_sections = get_voice_sections(audio_data, threshold)
    return time_voice_sections

def read_audio_path(audio_path: str) -> Dict[str, Any]:
    """
    Read an audio path, transform it and return a dict of data.

    :param audio_path: audio file path.
    :return: dict of data: *signal* (array of floats), sampling *rate* (integer) and *top db* (float).
    """
    audio_signal, sampling_rate = librosa.load(audio_path)
    transform = librosa.stft(audio_signal)
    db = librosa.amplitude_to_db(numpy.abs(transform))
    top_db = numpy.max(abs(db))
    return {"signal": audio_signal, "rate": sampling_rate, "top db": top_db}

def find_best_threshold(audio_data: Dict[str, Any], method: str, parameter: str) -> float:
    """
    Find the best threshold of audio data for the chosen method and parameter. For all methods, if the result is higher than top db, it is lowered to the latter.

    :param audio_data: dict of audio data.
    :param method: chunking method: *duration* (highest threshold where all voice sections are shorter than duration), *offset* (top db − offset), *threshold* (fixed threshold).
    :param parameter: parameter of the chosen method.
    :return: calculated threshold for method and parameter.
    """
    assert method in ["duration", "offset", "threshold"], f"Incorrect method ({method})."
    if method == "duration":
        continuum = get_continuum(audio_data, parameter)
        thresholds = [division["threshold"] for division in continuum if division["size"] == division["limited size"]]
        threshold = max(thresholds) if thresholds else audio_data["top db"]
    elif method == "offset":
        threshold = audio_data["top db"] - parameter if parameter < audio_data["top db"] else audio_data["top db"]
    elif method == "threshold":
        threshold = parameter if parameter < audio_data["top db"] else audio_data["top db"]
    return threshold

def get_continuum(audio_data: Dict[str, Any], max_duration: float, size: int = 20) -> List[Dict[str, Any]]:
    """
    Calculate the continuum (of chosen size) of voice sections (timestamps) depending on max duration limit.

    :param audio_data: dict of audio data.
    :max_duration: duration limit (in seconds).
    :return: a list of dicts of useful data: *timestamps* (in seconds) of voice sections, *threshold*, *durations* of voice sections, *size* (number of voice sections) and *limited size* (number of voice sections shorter than duration).
    """
    thresholds = numpy.array(audio_data["top db"]) - range(size)
    values = []
    for index, threshold in enumerate(thresholds):
        timestamps = get_voice_sections(audio_data, threshold)
        durations = [end - begin for begin, end in timestamps]
        limited_durations = [duration for duration in durations if duration <= max_duration]
        values.append({
            "timestamps": list(timestamps),
            "threshold": threshold,
            "durations": durations,
            "size": len(durations),
            "limited size": len(limited_durations)})
    return values

def get_voice_sections(audio_data: Dict[str, Any], threshold: float) -> List[Tuple[float, float]]:
    """
    Find the voice sections (in seconds) of an audio data according to a threshold.

    :param audio_data: dict of audio data.
    :param threshold: chosen threshold for voice section detection.
    :return: a list of tuples of voice sections (timestamps of start and end).
    """
    frame_voice_sections = librosa.effects.split(audio_data["signal"], top_db=threshold)
    time_voice_sections = [(start/audio_data["rate"], end/audio_data["rate"]) for index, (start, end) in enumerate(frame_voice_sections, 1)]
    return time_voice_sections
