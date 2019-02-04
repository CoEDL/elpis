def allowed_file(filenAPIame):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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