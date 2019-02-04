import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename
from ..blueprint import Blueprint
from . import comp
from ..paths import CURRENT_MODEL_DIR

bp = Blueprint("model", __name__, url_prefix="/model")
bp.register_blueprint(comp.bp)



@bp.route("/new")
def new():
    #assuming that this would only be a POST?
    this.models = state.Model()
    return '{"status": "new model created"}'

@bp.route("/name", methods=['GET', 'POST'])
def name():
    file_path = os.path.join(CURRENT_MODEL_DIR, 'name.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['name'])
    
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
    
    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "date": "{fin.read()}" }}'

@bp.route("/transcription-files")
def transcription_files():
    # setup the path
    path = os.path.join(CURRENT_MODEL_DIR, 'data')
    if not os.path.exists(path):
        os.mkdir(path)

    # handle incoming data
    if request.method == 'POST':
        print(f'Trans_files req: {request.json}')

    # return state update
    return f'{os.listdir(path)}'

@bp.route("/pronunciation")
def pronunciation():
    file_path = os.path.join(CURRENT_MODEL_DIR, 'pronunciation.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['pronunciation'])
    
    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "pronunciation": "{fin.read()}" }}'

@bp.route("/settings")
def settings():
    file_path = os.path.join(CURRENT_MODEL_DIR, 'settings.txt')
    if request.method == 'POST':
        # update the state name
        with open(file_path, 'w') as fout:
            fout.write(request.json['settings'])
    
    # return the state
    with open(file_path, 'r') as fin:
        return f'{{ "settings": "{fin.read()}" }}'


