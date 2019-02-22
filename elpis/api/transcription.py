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

bp = Blueprint("transcription", __name__, url_prefix="/transcription")

@bp.route("/new", methods=['GET', 'POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    t = kaldi.new_transcription(request.json["name"])
    m: Model = app.config['CURRENT_MODEL']
    t.link(m)
    app.config['CURRENT_TRANSCRIPTION'] = t
    return jsonify({
        "status": "ok",
        "data": t.config._load()
    })



@bp.route("/name", methods=['GET', 'POST'])
def name():
    t = app.config['CURRENT_TRANSCRIPTION']
    if t is None:
        # TODO sending a string error back in incorrect, jsonify it.
        return '{"status":"error", "data": "No current transcription exists (prehaps create one first)"}'
    if request.method == 'POST':
        t.name = request.json['name']
    return jsonify({
        "status": "ok",
        "data": t.name
    })

@bp.route("/transcribe-align", methods=['GET', 'POST'])
def transcribe_align():
    t: Transcription = app.config['CURRENT_TRANSCRIPTION']

    # handle incoming data
    if request.method == 'POST':

        file = request.files['file']
        t.transcribe_align(file)
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
