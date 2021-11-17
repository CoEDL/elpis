# Using the CLI Elpis Python API

Requires Docker.

## Prepare your data

Make a local directory with your data, including your training data, a letter to sound file if using Kaldi, and an untranscribed audio file if you are also transcribing.

> See example at https://github.com/CoEDL/dev-corpora

```
~/Desktop
    └── datasets
          └── abui
                ├── letter_to_sound.txt
                ├── transcribed
                │     ├── 1.eaf
                │     ├── 1.wav
                │     ├── 2.eaf
                │     └── 2.wav
                └── untranscribed
                     └── audio.wav
```


## Run Elpis, train and transcribe

Start Docker.

Run an Elpis docker container, sharing your local datasets directory with the container.

```
docker run --rm -it -p 5001:5001/tcp -v ~/Desktop/datasets:/datasets --entrypoint /bin/zsh coedl/elpis:latest
```


In the container, run the Python training script. It will look in the folder you gave, train a system based on the audio and text files it finds, and transcribe the untranscribed audio.

We have a demo script you can try. Base your own training script on this example.

```
python elpis/examples/cli/kaldi/train.py
```


Use the trained model to transcribe some audio.

```
python elpis/examples/cli/kaldi/transcribe.py
```
