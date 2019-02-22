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
    t= kaldi.new_transcription(request.json["name"])
    app.config['CURRENT_TRANSCRIPTION'] = t
    return jsonify({
        "status": "ok",
        "data": t.config._load()
    })

# @bp.route("/new", methods=['POST'])
# def new():
#     # assuming that this would only be a POST?
#     #this.models = state.Model()
#     return '{"status": "new model created"}'
#
#
# @bp.route("/name", methods=['GET', 'POST'])
# def name():
#     print(request.json['name'])
#     file_path = os.path.join(CURRENT_MODEL_DIR, 'name.txt')
#     if request.method == 'POST':
#         # update the state name
#         with open(file_path, 'w') as fout:
#             fout.write(request.json['name'])
#
#     # return the state
#     with open(file_path, 'r') as fin:
#         return f'{{ "name": "{fin.read()}" }}'
#
#
# @bp.route("/date", methods=['GET', 'POST'])
# def date():
#     file_path = os.path.join(CURRENT_MODEL_DIR, 'date.txt')
#     if request.method == 'POST':
#         # update the state name
#         with open(file_path, 'w') as fout:
#             fout.write(request.json['date'])
#
#     # return the state
#     with open(file_path, 'r') as fin:
#         return f'{{ "date": "{fin.read()}" }}'
#
#
# @bp.route("/usedModelName", methods=['GET', 'POST'])
# def usedModelName():
#     file_path = os.path.join(CURRENT_MODEL_DIR, 'usedModelName.txt')
#     if request.method == 'POST':
#         # update the state name
#         with open(file_path, 'w') as fout:
#             fout.write(request.json['usedModelName'])
#
#     # return the state
#     with open(file_path, 'r') as fin:
#         return f'{{ "usedModelName": "{fin.read()}" }}'
#
#
# @bp.route("/results", methods=['GET', 'POST'])
# def results():
#     file_path = os.path.join(CURRENT_MODEL_DIR, 'results.txt')
#     if request.method == 'POST':
#         # update the state name
#         with open(file_path, 'w') as fout:
#             fout.write(request.json['results'])
#
#     # return the state
#     with open(file_path, 'r') as fin:
#         return f'{{ "results": "{fin.read()}" }}'
#
#
# @bp.route("/audio", methods=['GET', 'POST'])
# def audio():
#     # setup the path
#     path = os.path.join(CURRENT_MODEL_DIR, 'current_transcription')
#     if not os.path.exists(path):
#         os.mkdir(path)
#
#     # handle incoming data
#     if request.method == 'POST':
#
#         file_ = request.files['file']
#         file_path = os.path.join(CURRENT_MODEL_DIR, file_.filename)
#         print(f'file name: {file_.filename}')
#
#         with open(file_path, 'wb') as fout:
#             fout.write(file_.read())
#             fout.close()
#
#         return file_.filename
