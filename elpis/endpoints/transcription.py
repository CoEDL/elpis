from flask import request, current_app as app, jsonify
from ..blueprint import Blueprint
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.model import Model
from elpis.wrappers.objects.transcription import Transcription
from elpis.wrappers.utilities import hasher

bp = Blueprint("transcription", __name__, url_prefix="/transcription")

@bp.route("/new", methods=['POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    t = kaldi.new_transcription(hasher.new()) # TODO transcriptions have no name
    m: Model = app.config['CURRENT_MODEL']
    t.link(m)
    app.config['CURRENT_TRANSCRIPTION'] = t
    file = request.files['file']
    t.transcribe_align(file, on_complete=lambda: print('Transcribed audio file!'))
    return jsonify({
        "status": "ok",
        "data": t.status
    })

@bp.route("/status", methods=['GET', 'POST'])
def status():
    t: Transcription = app.config['CURRENT_TRANSCRIPTION']
    return jsonify({
        "status": "ok",
        "data": t.status
    })

@bp.route("/elan", methods=['POST'])
def elan():
    t: Transcription = app.config['CURRENT_TRANSCRIPTION']
    return t.elan()

