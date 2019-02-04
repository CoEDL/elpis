import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename


ELPIS_ROOT_DIR = os.getcwd()
UPLOAD_FOLDER = os.path.join(ELPIS_ROOT_DIR, "Uploaded_files")
ALLOWED_EXTENSIONS = {'wav', 'eaf', 'trs', 'wordlist'}
bp = Blueprint("corpus", __name__, url_prefix="/corpus")


def allowed_file(filename):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def do():
    pass



""" 
POST functions: - Save incoming file to disk
"""
def save_file(folder_type):
    # file = request.files['file']
    uploaded_files = request.files.getlist("file[]")
    for file in uploaded_files:
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            continue
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder_type, filename))
            #######Should we just be using Model.add_audio_file here instead?
            #Model.add_audio_file
            # return redirect(url_for('corpus.wav',
                                    # filename=filename))
    return escape(repr(uploaded_files))



"""
GET functions:
"""
"""
- Return a list of all files of filetype
"""
def get_file_names(file_location):
    ########Should we be using the model.audio_files functions here?
    return '''<form method="POST" enctype="multipart/form-data" action="/corpus/">''' + file_location + '''
                <input type="file" name="file[]" multiple="">
                    <input type="submit" value="add">
                    </form>'''
    

"""
- Return speified file
"""
def get_file(file_location, filename):
    pass
    #Check that 
    #-- filename is not an illegal argument 
    #-- filename exists



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



"""
Settings Route
"""
@bp.route("/settings", methods=("GET", "POST"))
def settings(Model):
    if request.method == "POST":
            # Add settings for model
            state.add_settings(Settings) 
            return 200
    elif request.method == "GET":
        # Returns all model settings
        state.settings.get_settings()
        return 200


