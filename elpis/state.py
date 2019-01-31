import os
from typing import List, TextIO as TextFile
from .paths import MODELS_DIR
    
def filter_filenames(filenames: List[str]) -> List[str]:
    return [x.split('/')[-1] for x in filenames]



class State(object):
    def __init__(self):
        super()


class Settings(object):
    def __init__(self):
        super()
        #Model Settings
        self._audio_frequency = 44100
        self._mfcc = 22050
        self._ngram = 3
        self._beam = 10
    
    """
    How do I make sure SETS are called before GETS
    """

    # "Audio"
    # @property
    # def set_audio_frequency(frequency):
    #     self._audio_frequency = frequency
    
    # def get_audio_frequency():
    #     return self._audio_frequency
    
    # "MFCC"
    # @property
    # def set_mfcc(mfcc):
    #     self._mfcc = mfcc
    
    # def get_audio_frequency():
    #     return self._mfcc

    # "N-Gram"
    # @property
    # def set_ngram(ngram):
    #     self._ngram = ngram
    
    # def get_ngram():
    #     return self._ngram

    # "Beam"
    # @property
    # def set_beam(beam):
    #     self._beam = beam
    
    # def get_beam():
    #     return self._beam

    "Settings"
    def set_settings(settings):
        self._audio_frequency = settings[0]
        self._mfcc = settings[1]
        self._ngram = settings[2]
        self._beam = settings[3]

    def get_settings():
        return [
            self._audio_frequency, 
            self._mfcc,
            self._ngram,
            self._beam
        ]
        

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
    def __init__(self, location: str):
        """ Create the model state.

        :param name: name of the model. Must be unique.
        """
        super()

        self._location = location
        self._PATH_AUDIO = os.path.join(location, 'audio')
        self._PATH_TRANSCRIPTION = os.path.join(location, 'transcription')
        self._PATH_ADDITIONAL_TEXT = os.path.join(location, 'additional')
        self._PATH_PRONUNCIATION = os.path.join(location, 'pronunciation')
        
        if not os.path.exists(location):
            os.mkdir(self._PATH_AUDIO)
            os.mkdir(self._PATH_TRANSCRIPTION)
            os.mkdir(self._PATH_ADDITIONAL_TEXT)
            os.mkdir(self._PATH_PRONUNCIATION)

        #Model
        self._name: str = None
        self._date: str = None
        
        
    
    @property
    def name(self) -> str:
        if self._name is None:
            raise ValueError("name has not been set")
        return self._name

    @name.setter
    def name(self, value: str):
        with open(f'{self._location}/name', 'w') as fin:
            fin.write(value)
            self._name = value
    
    @property
    def audio_files(self):
        return os.listdir(self._PATH_AUDIO)

    @property
    def transcription_files(self):
        return os.listdir(self._PATH_TRANSCRIPTION)

    @property
    def additional_text_files(self):
        return os.listdir(self._PATH_ADDITIONAL_TEXT)

    @property
    def pronunciation(self):
        with open(self._PATH_PRONUNCIATION, 'rb') as fin:
            return fin.read().decode('utf-16')

    @pronunciation.setter
    def pronunciation(self, content: bytes):
        with open(self._PATH_PRONUNCIATION, 'wb') as fout:
            return out.write(content)

    @property
    def date(self) -> str:
        if self._date is None:
            raise ValueError("date has not been set")
        return self._date

    @date.setter
    def date(self, value: str):
        with open(f'{self._location}/date', 'w') as fin:
            fin.write(value)
            self._date = value

    def add_audio_file(filename: str, content: bytes):
        with open(f'{self._PATH_AUDIO}/{filename}', 'wb') as fout:
            fout.write(content)
    
    def add_transcription_file(filename: str, content: bytes):
        with open(f'{self._PATH_TRANSCRIPTION}/{filename}', 'wb') as fout:
            fout.write(content)

    def add_additional_text_file(filename: str, content: str):
        with open(f'{self._PATH_ADDITIONAL_TEXT}/{filename}', 'w') as fout:
            fout.write(content)

    def get_audio_file():
        return None

    def get_transcription_file():
        return None

    def get_additional_text_file():
        return None

    def get_pronunciation_file():
        return None

    

    

class Transcription(object):
    def __init__(self):
        super()
    
    @property
    def name():
        pass
    
    @property
    def model():
        pass

    @property
    def audio():
        pass

def load_existing_models() -> List[Model]: #corpus?
    return []
