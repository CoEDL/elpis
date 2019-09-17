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
    transcription = kaldi.new_transcription(hasher.new())  # TODO transcriptions have no name
    model: Model = app.config['CURRENT_MODEL']
    transcription.link(model)
    app.config['CURRENT_TRANSCRIPTION'] = transcription
    file = request.files['file']
    transcription.prepare_audio(file, on_complete=lambda: print('Prepared audio file!'))
    return jsonify({
        "status": "ok",
        "data": transcription.status
    })

@bp.route("/transcribe", methods=['GET','POST'])
def transcribe():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    transcription.transcribe(on_complete=lambda: print('Transcribed text!'))
    return jsonify({
        "status": "ok",
        "data": transcription.status
    })


@bp.route("/transcribe-align", methods=['GET','POST'])
def transcribe_align():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    transcription.transcribe_align(on_complete=lambda: print('Transcribed and aligned!'))
    return jsonify({
        "status": "ok",
        "data": transcription.status
    })


@bp.route("/status", methods=['GET', 'POST'])
def status():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    return jsonify({
        "status": "ok",
        "data": transcription.status
    })


@bp.route("/text", methods=['POST'])
def text():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    return transcription.text()

@bp.route("/elan", methods=['POST'])
def elan():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    return transcription.elan()
