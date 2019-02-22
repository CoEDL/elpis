import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape, current_app as app, jsonify
from werkzeug.utils import secure_filename
from ..blueprint import Blueprint
from ..paths import CURRENT_MODEL_DIR
import json
from ..kaldi.interface import KaldiInterface
from ..kaldi.model import Model
from ..kaldi.transcription import Transcription
from ..kaldi import hasher

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

