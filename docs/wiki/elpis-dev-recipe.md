# How to setup repositories to develop Elpis

This guide can assist in setting up directory structures to load repositories into a Docker container, enabling you to develop code and interact with the changes. This guide doesn't cover testing.

The recommended folder structure is to have a `~/sandbox` folder inside your user directory. This can contain the `elpis` Git repository, the `espnet` repository and the `state` folder to view the state that the program generates.

## Prepare your local dirs

Get the repos for developing, `git pull` etc if you need.

```shell
mkdir ~/sandbox
cd ~/sandbox
git clone --depth=1 https://github.com/CoEDL/elpis.git
git clone --depth=1 -b elpis https://github.com/persephone-tools/espnet
```

## Build the GUI

The Docker container has a build of the React app GUI in it. If you are cloning the elpis repository and working on the GUI, run these commands to enable changes to the GUI code to be reloaded in the browser.

```shell
cd ~/sandbox/elpis/elpis/gui
npm install && npm run watch
```

## Mount local dirs into existing image.

Run the Elpis Docker image. Mount your local repositories into the container. Leave out the mounts you aren't actively developing. Thus you get to use the venv in the Docker container, don't need to set up your own, avoiding version issues.

```shell
docker run --rm -it -p 5000:5000/tcp \
	-v ~/sandbox/state:/state \  
	-v ~/sandbox/elpis:/elpis \  
	--entrypoint zsh coedl/elpis:latest
```

Run these inside the container (setup earlier) to install stuff.

```shell
export FLASK_APP=elpis && flask run --host=0.0.0.0 --port=5000
```

You can also simply use the alias command inside the container.
```shell
run
```

## Command-line window

`elpis` uses `poetry` for dependency management and packaging. Starting up the virtual environment might be useful if you want to develop in an IDE or text editor with autocompletion & other fancy stuff, or if you would like to run tests.

```shell
cd ~/sandbox/elpis
poetry shell
poetry update
```

## Monitor the app/code

Open a new Terminal and get another window into the running Elpis container using this (this works on Mac, untested on PC)

```shell
docker exec -it $(docker ps -q) bash
```

### CUDA (beta, for ESPnet).

If you have a CUDA-compatible GPU it is possible to achieve better performance by utilising the GPU in training your models. For this purpose, CUDA driver and runtime must be installed on host machine (more informations [here](https://www.celantur.com/blog/run-cuda-in-docker-on-linux/) and [there](https://github.com/NVIDIA/nvidia-docker)):

Driver installation – if necessary (XXX is the version number):

```shell
sudo apt-get install nvidia-driver-XXX
```

Runtime installation (beware of distributions not yet supported…):

```shell
curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list |\
    sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update
sudo apt-get install nvidia-container-runtime
```

But sometimes an older version (like *ubuntu20.04* runtime on your Ubuntu 20.10 distribution) can work, so you can try to force the distribution variable if necessary, for example with:

```shell
curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -
distribution=ubuntu20.04
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list |\
    sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update
sudo apt-get install nvidia-container-runtime
```

Then you can try the CUDA-specific Dockerfile (`gpu/Dockerfile` in root folder):

```shell
cd ~/sandbox/elpis
docker build . --file gpu/Dockerfile --tag coedl/elpis-cuda:latest > build.log
```

(It will write all logs in `build.log` file, because it is not so trivial to make it work flawlessly.)

Then, run it by adding the `--gpus all` argument in `docker run`:

```shell
docker run --gpus all -it -p 5000:5000/tcp \
    -v ~/sandbox/elpis:/elpis \
    -v ~/sandbox/espnet/egs/elpis:/espnet/egs/elpis \
    -v ~/sandbox/espnet/utils/:/espnet/utils/ \
    --entrypoint /bin/zsh \
    coedl/elpis-cuda:latest
```

**This feature is currently in a beta stage. Utilising the GPU for training is only currently recommended for those who know what they're doing or those particularly interested in achieving higher performance.**