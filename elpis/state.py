from typing import List

class State(object):
    def __init__(self):
        super()
    



class Model(object):
    """
    Stores the state of the model.

    Properties:
        name:
            A unique name for the model.
        audio_files:
            list of *wav* files containing the audio the transcription was
            developed from.
        transcription_files:
            elan files that match to the wav files
        additional:
    
    Files from `audio_files`, `transcription_files`, and `additional` must
    exist on the server before being added to the variables.

    `audio_files` and `transcription_files` must have paired names.
            
    """
    def __init__(self, name: str):
        """ Create the model state.

        :param name: name of the model. Must be unique.
        """
        super()
        self.name: str = name
        self.audio_files: List[str] = []
        self.transcription_files: List[str] = []
        self.additional: List[str] = []
        #check that audio and transcript filenames match up


class Transcription(object):
    def __init__(self):
        super()
    @property
    def name():
        pass

class audio

class transcript

class additional 