# How to setup repositories to develop Elpis

This guide can assist in setting up directory structures to load repositories into a Docker container, enabling you to develop code and interact with the changes. This guide doesn't cover testing.


## Prepare your local dirs

Get the repos for developing, `git pull` etc if you need.

```
mkdir ~/elpis-sandbox
cd ~/elpis-sandbox
git clone --depth=1 https://github.com/CoEDL/elpis.git
git clone --depth=1 https://github.com/CoEDL/elpis-gui.git
git clone --depth=1 https://github.com/persephone-tools/persephone
git clone --depth=1 -b elpis https://github.com/persephone-tools/espnet
```


## Build the GUI

The Docker container has a build of the React app GUI in it, but if you are cloning the GUI repository and replacing the directory in the container with the local repository, the app build directory won't exist in the container (it is excluded from version control so it isn't in what you cloned). Run these commands to install the NPM libraries required, and to build a production version of the GUI into the `elpis-gui/build` dir. If you are developing the GUI, replace `npm run build` with `npm run watch` and then when you make changes to the GUI code, you'll get an automatic rebuild of the app. You will need to manually reload the browser that has the interface. 

```
cd elpis-gui
npm install && npm run build
```


## Mount local dirs into existing image. 
Run the Elpis Docker image. Mount your local repositories into the container. Leave out the mounts you aren't actively developing. Thus you get to use the venv in the Docker container, don't need to set up your own, avoiding version issues.

```
docker run -it -p 5000:5000/tcp \
    -v ~/elpis-sandbox/elpis:/elpis \
    -v ~/elpis-sandbox/elpis-gui:/elpis-gui \
    -v ~/elpis-sandbox/persephone:/elpis/persephone \
    -v ~/elpis-sandbox/espnet/egs/elpis:/espnet/egs/elpis \    
    --entrypoint /bin/bash \
    coedl/elpis:latest
```


## Run the app

Run these inside the container to install stuff.

```
source /venv/bin/activate
python setup.py develop
export FLASK_APP=elpis && flask run --host=0.0.0.0 --port=5000
```


## Monitor the app/code

Open a new Terminal and get another window into the running Elpis container using this (this works on Mac, untested on PC)

```
docker exec -it $(docker ps -q) bash
```
