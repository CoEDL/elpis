from elpis.wrappers.objects.fsobject import FSObject
from elpis.wrappers.objects.interface import KaldiInterface
from pathlib import Path

# Get prior model
kaldi = KaldiInterface('/elpis/state')
m = kaldi.get_model('mx')

# Make a transcription interface and transcribe unseen audio to elan.
t = kaldi.new_transcription('tx')
t.link(m)
with open('/recordings/untranscribed/audio.wav', 'rb') as faudio:
    t.prepare_audio(faudio)
# t.transcribe_align()
# print(t.elan().decode('utf-8'))
t.transcribe()
print(t.text().decode('utf-8'))
