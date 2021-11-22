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



## Setting SSH key

To fix `Remote Host changed` error, delete these files from your local machine.
```shell
~/.ssh/google_compute_engine
~/.ssh/google_compute_engine.pub
~/.ssh/google_compute_known_hosts
```

Then recreate them. Start the VM in the browser interface. Login and generate new SSH keys.
```shell
gcloud auth login
gcloud compute ssh --zone "us-central1-c" "instance-3"  --tunnel-through-iap --project "elpis-workshop"
``` 



## Viewing Tensorboard on GCP

Connect to the tensorboard that shows train loss (currently in the HFT branch).

* Add a Firewall rule in `GCP > VPC networks > Firewall` for TCP port `6006` using a tagname `firewall`.
* Create/edit a VM instance.
* Include the `firewall` tagname in the list of VM Network tags.
* Start the VM and connect to it. `gcloud compute ssh instance-3`
* Start Docker and expose the 6006 port. `docker run --gpus all -it -p 80:5001/tcp -p 6006:6006/tcp --entrypoint /bin/zsh coedl/elpis:hft`
* Run Tensorboard with host arg. `tensorboard --logdir=/state/models/MODEL-HASH/runs --port 6006 --host=0.0.0.0`
