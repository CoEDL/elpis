# Handy GCP commands

Follow [these instructions](https://cloud.google.com/sdk/docs/install) to install the `gcloud` tool.


## Connect to a Virtual Machine

Use `gcloud` to connect from a local terminal to a Google Cloud Platform Virtual Machine. `gcloud init` will authorise gcloud to use your credentials to access your account. Then we will list the available machines, and make an SSH connection to one. Change `instance-1` in the code below to match the name of the machine you want to connect to.
```
gcloud init
gcloud compute instances list
gcloud compute ssh instance-1
```


## Using screen

Using screen will avoid long-running training processes from terminating due to network connection failures between your machine and the VM.

Start screen.
```
screen
```

Do things, e.g. run a Docker container...

Then detach or reattach after a network failure.  
* `Ctrl-a` + `Ctrl-d` to detach from the screen  
* `screen -ls` to list screens  
* `screen -r` to reattach  


## Copy model files from GCP

SSH to GCP instance.  

Get into the docker container.
```
docker exec -it elpis zsh
cd /state/of_origin/models
ls
tar -cvf model.tar HASH_DIR_NAME
```

Keep that Docker container running, and in another SSH terminal, copy from the container to the host.
```
docker cp elpis:/state/of_origin/models/model.tar .
```

Copy from the host to the local machine (do this in a local terminal window).
```
gcloud compute scp instance-1:~/model.tar ~/Downloads/model.tar
```

Otherwise, could share state dir from host into docker and save a few steps...


## Fixing the SSH Key

When making an SSH connection using gcloud, you may receive a `Remote Host changed` error. This can be fixed by regenerating some files on your computer.

Use the Google Cloud Console in your browser to check that the VM is running.

Delete these files from your computer.
```shell
~/.ssh/google_compute_engine
~/.ssh/google_compute_engine.pub
~/.ssh/google_compute_known_hosts
```

Run these commands on your computer to authorise you and generate new SSH keys. Replace the zone, instance and project names to suit your situation.
```shell
gcloud auth login
gcloud compute ssh --zone "us-central1-c" "instance-1"  --tunnel-through-iap --project "elpis-workshop"
``` 
