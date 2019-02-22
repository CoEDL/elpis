from kaldi.interface import KaldiInterface


kaldi = KaldiInterface('/elpis/state')

ds = kaldi.new_dataset('dsy')
with open('/elpis/abui_toy_corpus/data/1_1_4.eaf', 'rb') as feaf, open('/elpis/abui_toy_corpus/data/1_1_4.wav', 'rb') as fwav:
    ds.add_fp(feaf, 'f.eaf')
    ds.add_fp(fwav, 'f.wav')
ds.process()

def transcribe():
    t = None
    def complete():
        print(t.elan().decode('utf-8'))
    t = kaldi.new_transcription('tx')
    t.link(m)
    t.transcribe_align('/elpis/abui_toy_corpus/data/1_1_1.wav', on_complete=complete)

m = kaldi.new_model('mx')
m.link(ds)
m.set_l2s_path('/elpis/abui_toy_corpus/config/letter_to_sound.txt')
m.generate_lexicon()
m.train(on_complete=transcribe)
