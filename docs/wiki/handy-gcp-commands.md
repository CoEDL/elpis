# Handy GCP commands


## Use screen to run in background 

SSH to GCP instance.

Start screen.
```
screen
```

Run Docker container.
```
docker run --gpus all -it -p 80:5000/tcp --entrypoint /bin/zsh coedl/elpis:ben-hft-gpu
```

Do things...

Then,  
* `Ctrl-a` + `Ctrl-d` to detach from the screen  
* `screen -ls` to list screens  
* `screen -r` to reattach  


## Copy model files from GCP

SSH to GCP instance.  

Get into the docker container.
```
docker exec -it $(docker ps -q) zsh
cd /state/models
ls
tar -cvf model.tar HASH_DIR_NAME
```

Keep that Docker container running, and in another SSH terminal, copy from the container to the host.
```
docker cp $(docker ps -q):/state/models/model.tar .
```

Copy from the host to the local machine (do this in a local terminal window).
```
gcloud compute scp instance-3:~/model.tar ~/Downloads/model.tar
```


Otherwise, could share state dir from host into docker and save a few steps...
