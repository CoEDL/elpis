class Transcription(object):
    def __init__(self, name, model, audio):
        #super()
        self._name = name
        self._model = model
        self._audio = audio
    
    "Name"
    @property
    def set_name(name):
        self._name = name
    
    def get_name():
        return self._name
    
    "Model"
    @property
    def set_model(name): #necessary?
        self._name = name
    
    def get_name():
        return self._model

    "Audio"
    @property
    def set_audio(audio):
        self._audio = audio
    
    def get_audio():
        return self._audio
    