# Using the CLI Elpis Python API

**Note: this guide is not up to date with the monorepo structure** 

Requires Docker.

## Prepare your data

Make a local directory with
- letter to sound file
- your training data
- untranscribed audio file.

> See example at https://github.com/CoEDL/dev-corpora

```
~/Desktop
    └── recordings
       ├── letter_to_sound.txt
       ├── transcribed
       │       ├── 1.eaf
       │       ├── 1.wav
       │       ├── 2.eaf
       │       └── 2.wav
       └── untranscribed
       		     └── audio.wav
```


## Run Elpis, train and transcribe

Start Docker.

Run an Elpis docker container, sharing your local recordings directory with the container.

```
docker run --rm -it -p 5001:5001/tcp -v ~/Desktop/recordings:/recordings --entrypoint /bin/bash coedl/elpis:0.94.0
```


In the container, run the Python training script. it will look in the folder you gave, and train a system based on the audio and text files it finds. We have a demo script you can try. Base your own training script on this example.

```
python examples/cli/elan/train.py
```


Use the trained model to transcribe some audio.

```
python examples/cli/transcribe.py
```



## Notes

If you are developing Elpis, you can also mount a local copy of Elpis into the contianer. See the wiki for more deluxe method of developing with VS Code.

```
docker run --rm -it -p 5001:5001/tcp -v ~/sandbox/elpis:/elpis -v ~/sandbox/elpis-gui:/elpis-gui -v ~/Desktop/recordings:/recordings  --entrypoint /bin/bash coedl/elpis:0.94.0
```


Prepare for using the CLI. This installs Elpis as an operating system site package. Do this in the Docker container. 

```
python3 -m venv venv
source venv/bin/activate
python setup.py develop
```


