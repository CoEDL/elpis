import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename
from ..blueprint import Blueprint
from . import comp
from ..paths import CURRENT_MODEL_DIR
import json

bp = Blueprint("transcriptions", __name__, url_prefix="/transcriptions")
bp.register_blueprint(comp.bp)


@bp.route("/new", methods=['POST'])
def new():
    # assuming that this would only be a POST?
    #this.models = state.Model()
    return '{"status": "new model created"}'

@bp.route("/name", methods=['GET', 'POST'])
def name():
    print(request.json['name'])
    file_path = os.path.join(CURRENT_MODEL_DIR, 'name.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['name'])

    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "name": "{fin.read()}" }}'


@bp.route("/date", methods=['GET', 'POST'])
def date():
    file_path = os.path.join(CURRENT_MODEL_DIR, 'date.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['date'])

    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "date": "{fin.read()}" }}'


@bp.route("/usedModelName", methods=['GET', 'POST'])
def usedModelName():
    file_path = os.path.join(CURRENT_MODEL_DIR, 'usedModelName.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['usedModelName'])

    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "usedModelName": "{fin.read()}" }}'

@bp.route("/results", methods=['GET', 'POST'])
def results():
    file_path = os.path.join(CURRENT_MODEL_DIR, 'results.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['results'])

    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "results": "{fin.read()}" }}'

@bp.route("/audio", methods=['GET', 'POST'])
def audio():
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
            print(f'file: {file}')
            print(f'file name: {file.filename}')
            file_names.append(file.filename)

    # return just the received file names
    # and let the GUI append or overwrite
    # or else, send back the filenames of all input files
    return json.dumps(file_names)