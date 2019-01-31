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


def get_and_set(folder_dir, *filename):
    if request.method == "POST":
        # Process incoming wav file
        save_file(folder_dir)
        return 200
    elif request.method == "GET":
        if not filename:
            # Return a list of all elan files
            get_file_names(folder_dir)
            return 200
        else:
            # Return specific file from list
            get_file(folder_dir, filename)
   
    # if request.method == "POST":
    #     # Process incoming wav file
    #     save_file(Model.audio_files)
    #     return 200
    # elif request.method == "GET":
    #     if not filename:
    #         # Return a list of all elan files
    #         get_file_names(Model.audio_files)
    #         return 200
    #     else
    #         # Return specific file from list
    #         get_file(Model.audio_files, filename)

"""
Audio Files
"""
@bp.route("/wav", methods=("GET", "POST"))
def wav(Model, *filename):
    if not filename: 
        get_and_set(Model.audio_files) 
    else: get_and_set(Model.audio_files, filename)
   
        

"""
Transcriptions
"""
@bp.route("/elan", methods=("GET", "POST"))
def elan(Model, *filename):
    if not filename:
        get_and_set(Model.transcription_files)
    else: get_and_set(Model.transcription_files, filename)
        


@bp.route("/trs", methods=("GET", "POST"))
def trs(Model, *filename):
    if not filename:
        get_and_set(Model.transcription_files)
    else: get_and_set(Model.transcription_files, filename)


@bp.route("/wordlist", methods=("GET", "POST"))
def wordlist(Model, *filename):
    if not filename:
        get_and_set(Model.transcription_files)
    else: get_and_set(Model.transcription_files, filename)

@bp.route("/name", methods=("GET", "POST"))
def name_test():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        with open('name_file', 'w') as fout:
            fout.write(request.json['name'])
        with open('name_file', 'r') as fin:
            return '{"name": "' + fin.read() + '"}'
        return ''
    else:
        return "Error"

    

# """
# Additional Text
# """
# @bp.route("/txt", methods=("GET", "POST"))
# def wordlist(Model, *filename):
#     if not filename:
#         get_and_set(Model.additional_text_files)
#     else: get_and_set(Model.additional_text_files, filename)


"""
Pronunciation
"""
#What filetype is this?


