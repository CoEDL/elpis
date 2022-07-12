# Install Elpis on Google Cloud with GPU

If needed, do the "Setup you account" steps on the [Install Elpis on Google Cloud](install-elpis-on-gcp.md) wiki page. 


## Create a Virtual Machine 

The type of machine you can create depends on the quotas you have access to. 

[GPU quotas](https://console.cloud.google.com/iam-admin/quotas?authuser=2&project=elpis-workshop&folder&organizationId&metric=GPUs%20(all%20regions)&location=GLOBAL)

[all quotas](https://console.cloud.google.com/iam-admin/quotas?authuser=2&project=elpis-workshop)

For a basic machine, use these settings:
* GPU
* N1 series
* n1-standard-16 (16 vCPUs, 60 GB memory)
* 1 x NVIDIA Tesla T4 (approx $600/month)

* Standard persistent disk Ubuntu 20.04 approx 300GB
* Allow http traffic
* Add `tensorboard` to the `Networking, Disks, Security, Management, Sole-tenancy` > `Networking` > `Network tags` section
* Add the script below to the `Management` > `Startup scripts` section

```shell
# GPU startup script v0.3

# Check if this has been done before & skip if so
if [[ -f /etc/startup_installed ]];
then
  sudo chmod 666 /var/run/docker.sock
  exit 0;
fi


# Install CUDA

sudo apt install linux-headers-$(uname -r)
curl -O https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt update
sudo apt -y install cuda


# Install NVIDIA Container Toolkit

curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker

distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
sudo usermod -aG docker $USER
sudo chown $USER /var/run/docker.sock
sudo chmod 666 /var/run/docker.sock
docker pull coedl/elpis:latest

# Handy little app to check NVIDIA GPUs stats
sudo apt -y install nvtop

# Get elpis
cd ~
git clone https://github.com/CoEDL/elpis.git

# Will make it easier to copy model files etc out of the container
mkdir state

# Make a file which can be detected on next startup and thus skip doing this every time
touch /etc/startup_installed

echo "done"

```


This startup script will only run the first time the VM starts, to reduce the instance load time on subsequent restarts.


Don't use image deploy because this limits OS to container optimised, which prevents use of `--gpus all` docker run flag. To use `--gpus all` flag, we need to install specific version of nvidia drivers, not container optimised.




## Connect to the machine

View the VM logs to monitor the setup process. After the startup script has completed, SSH to the machine to create a Docker container and start Elpis.
Replace instance-1 with the name of your VM.

```
gcloud init
gcloud compute instances list
gcloud compute ssh instance-1
```


## Start Elpis

Run this command in the SSH connection to create a Docker container from the latest image, and start Elpis.

```
docker run --gpus all --name elpis --rm -it -p 80:5001/tcp coedl/elpis:latest
```

---

## Other handy scripts

Refer to the [Handy GCP commands](handy-gcp-commands.md) page for some handy scripts.


## Optionally, download and share data into the container

This may be helpful if you write a python file to run Elpis in the container and avoid the GUI.

Use the tool on [this page](https://angelov.ai/post/2020/wget-files-from-gdrive/) to create a wget command.

```
cd /
sudo mkdir na-elpis && cd na-elpis

sudo wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1tywUAtOUnAeITxC-YL61I5iTADIipeYS' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1tywUAtOUnAeITxC-YL61I5iTADIipeYS" -O data.zip && rm -rf /tmp/cookies.txt

sudo unzip data.zip

docker run --gpus all --name elpis -v /na-elpis:/na-elpis --rm -it -p 80:5001/tcp coedl/elpis:latest
```
