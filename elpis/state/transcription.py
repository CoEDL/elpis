class Transcription(object):
    def __init__(self, name, model, audio):
        self._name = name
        self._model = model
        self._audio = audio
    
    "Name"
    @property
    def set_name(self, name):
        self._name = name
    
    def get_name(self, ):
        return self._name
    
    "Model"
    @property
    def set_model(self, name): #necessary?
        self._name = name
    
    def get_name(self):
        return self._model

    "Audio"
    @property
    def set_audio(self, audio):
        self._audio = audio
    
    def get_audio(self):
        return self._audio
