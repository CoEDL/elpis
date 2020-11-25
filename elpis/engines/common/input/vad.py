import librosa
import numpy

def get_chunks(audio_path, method, parameter):
    audio_data = read_audio_path(audio_path)
    threshold = find_best_threshold(audio_data, method=method, parameter=parameter)
    print(f"""Top db = {audio_data["top db"]}, chosen threshold = {threshold} (method = {method})""")
    time_voice_sections = get_voice_sections(audio_data, threshold)
    return time_voice_sections

def get_voice_sections(audio_data, threshold):
    frame_voice_sections = librosa.effects.split(audio_data["signal"], top_db=threshold)
    time_voice_sections = [(start/audio_data["rate"], end/audio_data["rate"]) for index, (start, end) in enumerate(frame_voice_sections, 1)]
    return time_voice_sections

def get_continuum(audio_data, max_duration, size=20):
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

def read_audio_path(audio_path):
    audio_signal, sampling_rate = librosa.load(audio_path)
    transform = librosa.stft(audio_signal)
    db = librosa.amplitude_to_db(numpy.abs(transform))
    top_db = numpy.max(abs(db))
    return {"signal": audio_signal, "rate": sampling_rate, "top db": top_db}

def find_best_threshold(audio_data, method, parameter):
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
