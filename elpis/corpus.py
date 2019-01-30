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
POST functions:
"""
"""
- Save incoming file to disk
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
    #--filename is not an illegal argument 
    #-- filename exists




"""
Audio Files
"""
@bp.route("/wav", methods=("GET", "POST"))
def wav(Model, filename = ''):
    if request.method == "POST":
        # Process incoming wav file
        # file = request.files['file']
        save_file(Model._PATH_AUDIO)
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            get_file_names(Model._PATH_AUDIO)
            return 200
        else
            # Return specific file from list
            get_file(Model._PATH_TRANSCRIPTION, filename)
        

"""
Transcriptions
"""
@bp.route("/elan", methods=("GET", "POST"))
def elan(Model, filename = ''):
    if request.method == "POST":
        # Process incoming elan file
        save_file(Model._PATH_TRANSCRIPTION)
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            get_file_names(Model._PATH_AUDIO)
            return 200
        else
            # Return specific file from list
            get_file(Model._PATH_TRANSCRIPTION, filename)
        


@bp.route("/trs", methods=("GET", "POST"))
def trs(Model, filename = ''):
    if request.method == "POST":
        # Process incoming trs file
        save_file(Model._PATH_TRANSCRIPTION)
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            get_file_names(Model._PATH_AUDIO)
            return 200
        else
            # Return specific file from list
            get_file(Model._PATH_TRANSCRIPTION, filename)


@bp.route("/wordlist", methods=("GET", "POST"))
def wordlist(Model):
    if request.method == "POST":
        # Process incoming wordlist file
        save_file(Model._PATH_TRANSCRIPTION)
        TRANSCRIPTION_UPLOAD_FOLDER)
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            get_file_names(Model._PATH_AUDIO)
            return 200
        else
            # Return specific file from list
            get_file(Model._PATH_TRANSCRIPTION, filename)


"""
Additional Text
"""
@bp.route("/txt", methods=("GET", "POST"))
def wordlist(Model):
    if request.method == "POST":
        # Process incoming wordlist file
        save_file(Model._PATH_ADDITIONAL_TEXT)
        TRANSCRIPTION_UPLOAD_FOLDER)
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            get_file_names(Model._PATH_AUDIO)
            return 200
        else
            # Return specific file from list
            get_file(Model._PATH_TRANSCRIPTION, filename)

"""
Pronunciation
"""
#What filetype is this?


