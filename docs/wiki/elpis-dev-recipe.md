# How to setup repositories to develop Elpis

This guide can assist in setting up directory structures to load repositories into a Docker container, enabling you to develop code and interact with the changes. This guide doesn't cover testing.

The recommended folder structure is to have a `~/sandbox` folder inside your user directory. This can contain the `elpis` Git repository and a `state` folder to view the dataset, model and transcription sessions that the program generates.

This guide assumes the use of `zsh` rather than `bash`.

## Prepare your local dirs

Set up a `sandbox` folder in your home directory. Create a `state` folder in there. This will be shared into the Docker container when we run it soon.  

```shell
mkdir ~/sandbox
cd ~/sandbox
mkdir state
```

Clone the Elpis repo into the sandbox
```shell
git clone https://github.com/CoEDL/elpis.git
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
docker run --rm -it -p 5001:5001/tcp \
	-v ~/sandbox/state:/state \  
	-v ~/sandbox/elpis:/elpis \  
	--entrypoint zsh coedl/elpis:latest
```

Run this command to start the Elpis interface.
```shell
export FLASK_APP=elpis && flask run --host=0.0.0.0 --port=5001
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
docker exec -it $(docker ps -q) zsh
```
