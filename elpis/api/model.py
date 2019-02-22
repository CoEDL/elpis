import os
from flask import request, current_app as app, jsonify
from ..blueprint import Blueprint
from ..paths import CURRENT_MODEL_DIR
import json
import subprocess
from . import kaldi
from ..kaldi.interface import KaldiInterface
from ..kaldi.model import Model
from ..kaldi.dataset import Dataset

bp = Blueprint("model", __name__, url_prefix="/model")
bp.register_blueprint(kaldi.bp)


def run(cmd: str) -> str:
    import shlex
    """Captures stdout/stderr and writes it to a log file, then returns the
    CompleteProcess result object"""
    args = shlex.split(cmd)
    process = subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return process.stdout


@bp.route("/new", methods=['GET', 'POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    m = kaldi.new_model(request.json["name"])
    ds: Dataset = app.config['CURRENT_DATABUNDLE']
    m.link(ds)
    app.config['CURRENT_MODEL'] = m
    return jsonify({
        "status": "ok",
        "data": m.config._load()
    })


@bp.route("/name", methods=['GET', 'POST'])
def name():
    m = app.config['CURRENT_MODEL']
    if m is None:
        # TODO sending a string error back in incorrect, jsonify it.
        return '{"status":"error", "data": "No current model exists (prehaps create one first)"}'
    if request.method == 'POST':
        m.name = request.json['name']
    return jsonify({
        "status": "ok",
        "data": m.name
    })

@bp.route("/settings", methods=['GET', 'POST'])
def settings():
    m = app.config['CURRENT_MODEL']
    if m is None:
        # TODO sending a string error back in incorrect, jsonify it.
        return '{"status":"error", "data": "No current model exists (prehaps create one first)"}'
    if request.method == 'POST':
        m.ngram = request.json['ngram']
        # TODO make this an optional parameter
    return jsonify({
        "status": "ok",
        "data": {"ngram": m.ngram}})


@bp.route("/l2s", methods=['POST'])
def l2s():
    m: Model = app.config['CURRENT_MODEL']
    # handle incoming data
    if request.method == 'POST':
        file = request.files['file']
        if m is None:
            # TODO some of the end points (like this one) return files, but on error we still return a json string? Looks like bad practice to me
            return '{"status":"error", "data": "No current model exists (prehaps create one first)"}'
        m.set_l2s_fp(file)
    return m.l2s


@bp.route("/lexicon", methods=['GET', 'POST'])
def generate_lexicon():
    m: Model = app.config['CURRENT_MODEL']
    m.generate_lexicon()
    return m.lexicon


@bp.route("/list", methods=['GET', 'POST'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    return jsonify({
        "status": "ok",
        "data": kaldi.list_models()
    })

@bp.route("/status", methods=['GET', 'POST'])
def status():
    m: Model = app.config['CURRENT_MODEL']
    return jsonify({
        "status": "ok",
        "data": m.status
    })

@bp.route("/train", methods=['GET', 'POST'])
def train():
    m: Model = app.config['CURRENT_MODEL']
    m.train(on_complete=lambda: print("Training complete!"))
    return jsonify({
        "status": "ok",
        "data": m.status
    })


