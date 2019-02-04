bp_api = Blueprint("api/model", __name__, url_prefix="/api/model")


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
