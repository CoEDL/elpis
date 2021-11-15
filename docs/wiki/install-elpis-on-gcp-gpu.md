# Install on Google Cloud with GPU

## Check quotas

[GPU quotas](https://console.cloud.google.com/iam-admin/quotas?authuser=2&project=elpis-workshop&folder&organizationId&metric=GPUs%20(all%20regions)&location=GLOBAL)

[all quotas](https://console.cloud.google.com/iam-admin/quotas?authuser=2&project=elpis-workshop)


## Install requirements

### CPU

For CPU machines to use Kaldi, we just need to install Docker. Put this code into the VM instance startup script text area. When the machine starts, it will install Docker and download and run Elpis.

```
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
sudo apt install ./containerd.io_1.4.3-1_amd64.deb
sudo apt install -y docker-ce
sudo chmod 666 /var/run/docker.sock
sudo docker run -d --rm -p 80:5001/tcp coedl/elpis:latest
```


### GPU

For GPU, we need to install NVIDIA stuff. Rather than doing this in an install script, start the machine, SSH to it and then install CUDA and Docker.


#### Create a new VM

* GPU family
* N1 series
* n1-standard-16 (16 vCPUs, 60 GB memory)
* 1 x NVIDIA Tesla T4 (approx $600/month)

* Standard persistent disk Ubuntu 20.04 300GB
* Allow http traffic

Don't use image deploy because this limits OS to container optimised, which prevents use of `--gpus all` docker run flag. To use `--gpus all` flag, we need to install specific version of nvidia drivers, not container optimised.

Here's a command line version.
```
gcloud compute instances create instance-name --project=elpis-workshop --zone=us-central1-c --machine-type=n1-standard-16 --network-interface=network-tier=PREMIUM,subnet=default --maintenance-policy=TERMINATE --service-account=XXXXXXXXXXXX-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --accelerator=count=1,type=nvidia-tesla-t4 --tags=http-server --create-disk=auto-delete=yes,boot=yes,device-name=instance-5,image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20211102,mode=rw,size=200,type=projects/elpis-workshop/zones/us-central1-c/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any
```

#### After starting, ssh to the machine

```
gcloud init
gcloud auth login
gcloud config set project elpis-workshop
gcloud compute instances list
gcloud compute ssh instance-1
```


#### Install CUDA

From https://cloud.google.com/compute/docs/gpus/install-drivers-gpu#ubuntu-driver-steps

```
sudo apt install linux-headers-$(uname -r)
curl -O https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt update
sudo apt -y install cuda
```


#### Install Docker

From https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

```
curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker

distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

Verify the installation
```
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

Should give you something like 
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.57.02    Driver Version: 470.57.02    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla K80           Off  | 00000000:00:04.0 Off |                    0 |
| N/A   39C    P0    67W / 149W |      0MiB / 11441MiB |    100%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```


#### Set Docker permissions

```
sudo usermod -aG docker $USER
sudo chown $USER /var/run/docker.sock
sudo chmod 666 /var/run/docker.sock
```


#### Download/update Elpis

```
docker run --gpus all --name elpis --rm -it -p 80:5001/tcp coedl/elpis:ben-hft-gpu
```


#### Edit the model # epochs for dev sanity

Get into the container in another window

```
docker exec -it $(docker ps -q) zsh
```

Edit the model file, set `DEBUG=True`

```
vim /elpis/elpis/engines/hftransformers/objects/model.py
```

---


### Optionally, download and share data into the container

This may be helpful if you write a python file to run Elpis in the container and avoid the GUI.

Use this tool to create a wget command: https://gdrive-wget.glitch.me

```
cd /
sudo mkdir na-elpis && cd na-elpis

sudo wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1tywUAtOUnAeITxC-YL61I5iTADIipeYS' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1tywUAtOUnAeITxC-YL61I5iTADIipeYS" -O data.zip && rm -rf /tmp/cookies.txt

sudo unzip data.zip
```

```
docker run --gpus all --name elpis -v /na-elpis:/na-elpis --rm -it -p 80:5001/tcp coedl/elpis:ben-hft-gpu
```



