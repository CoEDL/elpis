import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename


ELPIS_ROOT_DIR = os.getcwd()
UPLOAD_FOLDER = os.path.join(ELPIS_ROOT_DIR, "Uploaded_files")
ALLOWED_EXTENSIONS = {'wav', 'eaf', 'trs', 'wordlist'}
bp_api = Blueprint("model", __name__, url_prefix="/api/model")


def allowed_file(filenAPIame):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
Audio File Routes
"""
@bp.route("/wav", methods=("GET", "POST"))
def wav(Model, *filename):
    if request.method == "POST":
        # Process incoming wav file
        state.add_audio_files(filename) 
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            state.audio_files()
            return 200
        else:
            # Return specific file from list
            state.get_audio_file(filename)
        

"""
Transcription Routes
"""
@bp.route("/elan", methods=("GET", "POST"))
def elan(Model, *filename):
    if request.method == "POST":
        # Process incoming wav file
        state.add_transcription_files(filename) 
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            state.transcription_files()
            return 200
        else:
            # Return specific file from list
            state.get_transcription_file(filename)
        


@bp.route("/trs", methods=("GET", "POST"))
def trs(Model, *filename):
    if request.method == "POST":
        # Process incoming wav file
        state.add_transcription_files(filename) 
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            state.transcription_files()
            return 200
        else:
            # Return specific file from list
            state.get_transcription_file(filename)


@bp.route("/wordlist", methods=("GET", "POST"))
def wordlist(Model, *filename):
    if request.method == "POST":
        # Process incoming wav file
        state.add_transcription_files(filename) 
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            state.transcription_files()
            return 200
        else:
            # Return specific file from list
            state.get_transcription_file(filename)
    

"""
Additional Text Route
"""
@bp.route("/additionaltxt", methods=("GET", "POST"))
def text(Model, *filename):
    if request.method == "POST":
        # Process incoming wav file
        state.add_additional_text_files(filename) 
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            state.additional_text_files()
            return 200
        else:
            # Return specific file from list
            state.get_additional_text_file(filename)


"""
Pronunciation Route
"""
@bp.route("/pronunciation", methods=("GET", "POST"))
def pronunciation(Model, *filename):
    if request.method == "POST":
        # Process incoming wav file
        state.add_pronunication_file(filename) 
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            state.pronunciation_file()
            return 200
        else:
            # Return specific file from list
            state.get_pronunication_file(filename)
