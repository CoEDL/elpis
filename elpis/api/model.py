import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename
from ..blueprint import Blueprint
from ..paths import CURRENT_MODEL_DIR
import json
import subprocess
from . import kaldi

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
        # cwd='/kaldi-helpers',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return process.stdout


@bp.route("/new", methods=['POST', 'GET'])
def new():
    # assuming that this would only be a POST?
    # this.models = state.Model()
    # TODO
    print('cmd output: ', run(f'rm -rf {CURRENT_MODEL_DIR}/*'))
    print(f'rm -rf {CURRENT_MODEL_DIR}/*')
    return '''{status: 'new model created'}'''


@bp.route("/name", methods=['GET', 'POST'])
def name():
    print(request.json['name'])
    file_path = os.path.join(CURRENT_MODEL_DIR, 'name.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['name'])
            fout.close()

        #result = subprocess.run(["ls -la"], stdout=subprocess.PIPE)
        # print(result.stdout)
    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "name": "{fin.read()}" }}'


@bp.route("/date")
def date():
    file_path = os.path.join(CURRENT_MODEL_DIR, 'date.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['date'])
            fout.close()
    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "date": "{fin.read()}" }}'


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

        filesOverwrite = request.form["filesOverwrite"]
        print('filesOverwrite:', filesOverwrite)

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
    # check the ./config directory structure is correct
    config_path = os.path.join(CURRENT_MODEL_DIR, 'config')
    if not os.path.exists(config_path):
        os.mkdir(config_path)
    opt_sil_file_path = os.path.join(config_path, 'optional_silence.txt')
    if not os.path.exists(opt_sil_file_path):
        with open(opt_sil_file_path, 'w') as fout:
            fout.write('SIL\n')
    sil_pho_file_path = os.path.join(config_path, 'silence_phones.txt')
    if not os.path.exists(sil_pho_file_path):
        with open(sil_pho_file_path, 'w') as fout:
            fout.write('SIL\nsil\nspn\n')

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


"""
Settings Route
"""
@bp.route("/settings", methods=("GET", "POST"))
def settings():
    file_path = os.path.join(CURRENT_MODEL_DIR, 'settings.txt')
    if request.method == "POST":

        run_settings_task_demo()
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
