# Using the CLI for Elpis GPU

**This doc refers to WIP on `hft` branch.** 

See the example script in `elpis/examples/cli/hft/train.py` for a simple demo of how to do data prep and training. 

The example script will used the bundled TIMIT data that is included in the `datasets` dir in the docker container root. 

The `hft` image comes with `abui`, `na` and `timit` data provided. See below for layout. To use your own data, add it as a subdir of `/datasets` and change the script `DATASET_DIR` value to suit. (To get your data into the container, use curl/wget/git clone.)

Running the sample script will prepare/normalise the data and do training. Subsequent runs of the script will reuse the prepared dataset, saving having to prepare the data repeatedly, and make a new training session.

If you prefer to redo data preparation, edit the Python script and change the `DATASET_NAME` value, while retaining the `DATASET_DIR` value. 

Once training is complete, the model files will be in a `/state/models/XXXXX` dir. 


### Commands

Connect to a GCP instance and run Elpis docker.

```
gcloud compute ssh instance-3
screen
docker run --gpus all --rm -it -p 80:5001/tcp --entrypoint /bin/zsh hft
git pull
python elpis/examples/cli/hft/train.py
```


To manipulate training params, open another terminal and modify the model.py file.

```
gcloud compute ssh instance-3
docker exec -it $(docker ps -q) zsh
vim /elpis/elpis/engines/hftransformers/objects/model.py
```


### Data layout

```
/
├── ...
├── datasets
│   │
│   ├── abui
│   │   ├── letter_to_sound.txt
│   │   ├── transcribed
│   │   │     ├── 1.eaf
│   │   │     ├── 1.wav
│   │   │     ├── 2.eaf
│   │   │     └── 2.wav
│   │   └── untranscribed
│   │         └── audio.wav
│   │
│   │
│   ├── na
│   │   ├── README.md
│   │   ├── transcribed
│   │   │     ├── CRDO-NRU_F4_10.eaf
│   │   │     └── CRDO-NRU_F4_10.wav
│   │   └── untranscribed
│   │         └── CRDO-NRU_F4.wav
│   │
│   │
│   └── timit
│       ├── dur.txt
│       ├── infer
│       │     ├── fadg0-sa1.eaf
│       │     ├── fadg0-sa1.txt
│       │     ├── falk0-sa2.txt
│       │     └── falk0-sa2.wav
│       ├── timit_l2s.txt
│       └── training_data
│             ├── fadg0-sa2.eaf
│             ├── fadg0-sa2.wav
│             └── ...
├── ...
├── ...
│
```
