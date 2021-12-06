from flask import request, current_app as app, jsonify
from ..blueprint import Blueprint
from elpis.engines import Interface
from elpis.engines.common.objects.model import Model
from elpis.engines.common.objects.transcription import Transcription
from elpis.engines.common.utilities import hasher
from loguru import logger

bp = Blueprint("transcription", __name__, url_prefix="/transcription")

# TODO transcriptions have no name
@bp.route("/new", methods=['POST'])
def new():
    interface: Interface = app.config['INTERFACE']
    transcription = interface.new_transcription(hasher.new())
    model: Model = app.config['CURRENT_MODEL']
    transcription.link(model)
    app.config['CURRENT_TRANSCRIPTION'] = transcription
    file = request.files['file']
    transcription.prepare_audio(file, on_complete=lambda: logger.info('Prepared audio file!'))
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
    transcription.transcribe(on_complete=lambda: logger.info('Transcribed text!'))
    data = {
        "status": transcription.status,
        "stage_status": transcription.stage_status
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
        "stage_status": transcription.stage_status,
        "type": transcription.type
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/text", methods=['GET'])
def text():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    data = {
        "audio_filename": transcription.audio_filename,
        "text": transcription.text()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/elan", methods=['GET'])
def elan():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    data = {
        "audio_filename": transcription.audio_filename,
        "elan": transcription.elan()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/confidence", methods=['GET'])
def confidence():
    transcription: Transcription = app.config['CURRENT_TRANSCRIPTION']
    data = {
        "confidence": transcription.get_confidence()
    }
    return jsonify({
        "status": 200,
        "data": data
    })
