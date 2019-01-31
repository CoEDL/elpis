class Settings(object):
    def __init__(self):
        super()
        #Model Settings
        self._audio_frequency = 44100
        self._mfcc = 22050
        self._ngram = 3
        self._beam = 10

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