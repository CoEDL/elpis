import json

from typing import Dict, List

from flask import request, make_response
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.errors import InterfaceError
from .utils.wrappers import require_dataset
from elpis.engines.common.utilities import load_json_file

bp = Blueprint("statistics", __name__, url_prefix="/statistics")

@bp.route("/frequency", methods=['GET'])
@require_dataset
def frequency(dataset: Dataset):
    """
    Returns the frequency of all words in a dataset, also known
    as the wordlist file.
    """
    #TODO(jack) support querying frequency across files
    fname = request.args.get("file")
    dataset.process() # Why do we need to run this each time? Can we cache?
    if fname is not None:
        # File specified, get the frequency of a specific file
        # We need to bork this, because filenames are stored with eaf extensions
        if (fname + ".eaf") not in dataset.config['files']:
            return jsonify({"status": 404,
                            "data": "File not found."})
        else:
            # A processed dataset stores a file `annotations.json` which contains
            # all transcriptions by file, check if each transcription belongs to requested file
            #TODO(jack) this search is linear, so for big datasets maybe needs optimisation
            annotations: List[Dict[str, str]] = load_json_file(f'{dataset.pathto.annotation_json}')
            frequency = {}
            #TODO(jack) slightly duplicated from dataset.py
            for transcription in annotations:
                if transcription['audio_file_name'] == (fname + ".wav"):
                    words = transcription['transcript'].split()
                    for word in words:
                        frequency[word] = frequency.get(word, 0) + 1
            return jsonify({"status": 200,
                            "frequency": frequency})
    else:
        # File not specified, get the frequency across the database
        with dataset.pathto.word_count_json.open() as fin:
            frequency = fin.read()
        data = {
            "frequency": frequency
        }
        return jsonify({
            "status": 200,
            "data": data
        })
