from .fsobject import FileSystemObject

class Transcription(FileSystemObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)