from elpis.wrappers.objects.interface import KaldiInterface

# Step 0
# ======
# Load an existing model
kaldi = KaldiInterface('/elpis/state')
m = kaldi.get_model('mx')
print("using model", m.name)

# Step 1
# ======
# Make a transcription interface and transcribe unseen audio to elan.
t = kaldi.new_transcription('tx')
t.link(m)
with open('/recordings/untranscribed/audio.wav', 'rb') as faudio:
    t.prepare_audio(faudio)
t.transcribe()
print(t.text().decode('utf-8'))
