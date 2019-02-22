import os
from flask import request, current_app as app, jsonify
from ..blueprint import Blueprint
from ..paths import CURRENT_MODEL_DIR
import json
import subprocess
from . import kaldi
from ..kaldi.interface import KaldiInterface
from ..kaldi.model import Model

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
    app.config['CURRENT_MODEL'] = m
    return jsonify({
        "status": "ok",
        "data": m.config._load()
    })


@bp.route("/name", methods=['GET', 'POST'])
def name():
    m = app.config['CURRENT_MODEL']
    if m is None:
        return '{"status":"error", "data": "No current model exists (prehaps create one first)"}'
    if request.method == 'POST':
        m.name = request.json['name']
    return jsonify({
        "status": "ok",
        "data": m.name
    })

@bp.route("/l2s", methods=['POST'])
def l2s():
    m: Model = app.config['CURRENT_MODEL']
    # handle incoming data
    if request.method == 'POST':
        file = request.files['file']
        if m is None:
            return '{"status":"error", "data": "No current model exists (prehaps create one first)"}'
        m.set_l2s_fp(file)
    return m.l2s

@bp.route("/lexicon", methods=['GET', 'POST'])
def generate_lexicon():
    m: Model = app.config['CURRENT_MODEL']
    m.generate_lexicon()
    return m.lexicon


def data_bundle():
    pass


# ------------------------------------------------------------------
# Everything under this ^ line is unchecked ( even this comment :O )


@bp.route("/transcription-files", methods=['GET', 'POST'])
def transcription_files():
    # setup the path
    path = os.path.join(CURRENT_MODEL_DIR, 'data')
    if not os.path.exists(path):
        os.mkdir(path)

    # handle incoming data
    if request.method == 'POST':

        # the request includes this filesOverwrite property
        # use this to determine whether received files are
        # appended to input data or overwrite input data
        # watch out for duplicate files if not overwriting!

        files_overwrite = request.form["filesOverwrite"]
        print('filesOverwrite:', files_overwrite)

        uploaded_files = request.files.getlist("file")
        file_names = []
        for file in uploaded_files:
            file_path = os.path.join(path, file.filename)
            with open(file_path, 'wb') as fout:
                fout.write(file.read())
                fout.close()
            file_names.append(file.filename)

            # return just the received file names
            # and let the GUI append or overwrite
            # or else, send back the filenames of all input files
            return json.dumps(file_names)


@bp.route("/pronunciation", methods=['POST'])
def pronunciation():

    # handle incoming data
    if request.method == 'POST':
        file = request.files['file']

        file_path = os.path.join(config_path, "letter_to_sound.txt")
        print(f'file name: {file.filename}')

        with open(file_path, 'wb') as fout:
            fout.write(file.read())
            fout.close()

        with open(file_path, 'rb') as fin:
            return fin.read()


@bp.route("/settings", methods=("GET", "POST"))
def settings():
    """
    Settings Route
    """
    file_path = os.path.join(CURRENT_MODEL_DIR, 'settings.txt')
    if request.method == "POST":
        # write settings to file
        print(f'settings: {request.json["settings"]}')
        with open(file_path, 'w') as fout:
            fout.write(json.dumps(request.json['settings']))
            fout.close()

        # Add settings for model
        # state.add_settings(Settings)
        return json.dumps(request.json['settings'])

    elif request.method == "GET":
        with open(file_path, 'r') as fin:
            data = json.load(fin)
        # state.settings.get_settings()
        return json.dumps(data)


@bp.route("/list", methods=['GET', 'POST'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    return jsonify({
        "status": "ok",
        "data": kaldi.list_models()
    })
