class Model(object):
    """
    Stores the state of the model.

    Properties:
        name:
            A unique name for the model.
        date:
            Date model was created
        audio_files:
            list of *wav* files containing the audio the transcription was
            developed from.
        transcription_files:
            elan files that match to the wav files
        additional text files:
            ...
        pronunication file:
            Maps pronunciations to characters/sets of characters
    
    Requirements:
        Files from: 
                `audio_files`, 
                `transcription_files`, 
                `additional_text` and 
                'pronunciation'
            must exist on the server before being added to the variables.

        The `audio_files` and `transcription_files` must have paired names.       
    """

    def __init__(self, location: str):
        """ Create the model state.

        :param name: name of the model. Must be unique.
        """
        super()

        "File Dir."
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

        "Model Parameters"
        self._name: str = None
        self._date: str = None
        self._settings = Settings()
        self._transcriptions = []
    
        
    """
    Name
    """ 
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
    
    """
    Date
    """
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


    """
    Get List of Filenames
    """
    @property
    def audio_files(self):
        return os.listdir(self._PATH_AUDIO)

    @property
    def transcription_files(self):
        return os.listdir(self._PATH_TRANSCRIPTION)

    @property
    def additional_text_files(self):
        return os.listdir(self._PATH_ADDITIONAL_TEXT)


    """
    Set Files to Model
    """
    def add_audio_file(filename: str, content: bytes):
        with open(f'{self._PATH_AUDIO}/{filename}', 'wb') as fout:
            fout.write(content)
    
    def add_transcription_file(filename: str, content: bytes):
        with open(f'{self._PATH_TRANSCRIPTION}/{filename}', 'wb') as fout:
            fout.write(content)

    def add_additional_text_file(filename: str, content: str):
        with open(f'{self._PATH_ADDITIONAL_TEXT}/{filename}', 'w') as fout:
            fout.write(content)

    @pronunciation.setter
    def pronunciation(self, content: bytes):
        with open(self._PATH_PRONUNCIATION, 'wb') as fout:
            return out.write(content)

    """
    Get Files from Model
    """
    def get_audio_file():
        return None

    def get_transcription_file():
        return None

    def get_additional_text_file():
        return None

    def get_pronunciation_file():
        return None
    
    @property
    def pronunciation(self):
        with open(self._PATH_PRONUNCIATION, 'rb') as fin:
            return fin.read().decode('utf-16')