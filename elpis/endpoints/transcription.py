from flask import request, current_app as app, jsonify
from ..blueprint import Blueprint
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.model import Model
from elpis.wrappers.objects.transcription import Transcription
from elpis.wrappers.utilities import hasher


bp = Blueprint("transcription", __name__, url_prefix="/transcription")

  # TODO transcriptions have no name
@bp.route("/new", methods=['POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    transcription = kaldi.new_transcription(hasher.new())
    model: Model = app.config['CURRENT_MODEL']
    transcription.link(model)
    app.config['CURRENT_TRANSCRIPTION'] = transcription
    file = request.files['file']
    transcription.prepare_audio(file, on_complete=lambda: print('Prepared audio file!'))
    data = {
        "status": transcription.status,
        "originalFilename": file.filename
    }
    return jsonify({
        "status": 200,
        "data": data
    })

@bp.route("/transcribe", methods=['GET'])
def transcribe():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    transcription.transcribe(on_complete=lambda: print('Transcribed text!'))
    data = {
        "status": transcription.status,
        "type": transcription.type
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/transcribe-align", methods=['GET'])
def transcribe_align():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    transcription.transcribe_align(on_complete=lambda: print('Transcribed and aligned!'))
    data = {
        "status": transcription.status,
        "type": transcription.type
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/status", methods=['GET'])
def status():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    data = {
        "status": transcription.status,
        "type": transcription.type
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/text", methods=['GET'])
def text():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    # TODO fix this to return json wrapper
    return transcription.text()


@bp.route("/elan", methods=['GET'])
def elan():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    # TODO fix this to return json wrapper
    return transcription.elan()
