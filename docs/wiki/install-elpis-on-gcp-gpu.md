# Install Elpis on Google Cloud with GPU

If this is your first time using Elpis on Google Cloud, follow the steps on the [Setup Google Cloud account](setup-google-cloud-account.md) page. 

This document will go through a process of enabling the network access required to view training progress with Tensorboard, and detail the steps to start a machine running Elpis.  

When you have finished using Elpis on a GCP virtual machine, make sure you stop it to prevent ongoing costs. 


## Enable network access 

Elpis uses Tensorboard to display training progress and plots. To enable us to view the Tensorboard page, we need to add a "firewall rule" in the Cloud console. 

Sign in to the console. If you have multiple projects, choose the one you want to work with.

In the left hand navigation menu, go to "VPC network > Firewall". Click "Create Firewall Rule" (blue button at the top of the page).

Use the following settings, then click Create. This will create a rule which our machine can use to enable browser traffic to reach the Tensorboard. 

* Name: tensorboard
* Direction of traffic: Ingress
* Target tags (make sure this is lowercase, and all one word): tensorboard
* Source IPv4 ranges: 0.0.0.0/0
* Protocols and ports: Specified protocols and ports
* TCP: 6006


## Create a Virtual Machine and run Elpis

Go to the `Compute Engine > VM instances` page.

To run Elpis, create an instance with the following settings. These resources will be adequate for a small amount of data, but may need to be increased depending on the quantity of your data. This configuration would cost approximately $600 to run all day, every day, for a month.

* Name: Give your instance a meaningful name, perhaps the name of the language you are training with.
* Region and zone: These can be left as is, or change to a location near you if required. Note that different regions may have different GPU options.
* Machine family: GPU
* GPU-type: NVIDIA T4
* Number of GPUs: 1
* Machine-type: n1-standard-16 (16 vCPUs, 60 GB memory)


Scroll down to the Boot disk section. Change the boot disk to use the following settings.

* Operating system: Ubuntu
* Version: Ubuntu 20.04 LTS z86/64
* Boot disk type: Standard persistent disk 
* Size (GB): 300

Scroll down to the "Firewall" settings. Tick `Allow http traffic`

Click "Advanced options" to open that section.

Click "Networking" to open that section.

Type `tensorboard` in the `Network tags` field. This will allow the virtual machine to use the Tensorboard firewall rule we created earlier. 

Scroll down and click on `Management`, and paste the following code into the `Automation Startup script` section. This code will install all the required software, download Elpis to the VM, and start Elpis. 

Note that we install this way, and not using image deploy because image deploy limits the OS to "container optimised", which prevents use of `--gpus all` docker run flag. To use `--gpus all` flag, we need to install specific version of nvidia drivers, not container optimised.
 

```shell
# GPU startup script v0.6.3

# Check if this has been done before. Skip driver installation if so, just run Elpis
if [[ -f /etc/startup_installed ]];
then
  sudo chmod 666 /var/run/docker.sock
  # Run Elpis (non-interactive so that Elpis starts automatically)
  docker run -d --rm --name elpis --gpus all -p 80:5001/tcp -p 6006:6006/tcp coedl/elpis:latest
  exit 0;
fi

# Otherwise, install all the things.. then run Elpis
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

# Download and run Elpis (non-interactive so that Elpis starts automatically)
docker run -d --rm --name elpis --gpus all -p 80:5001/tcp -p 6006:6006/tcp coedl/elpis:latest
```

This startup script will only run the first time the VM starts, to reduce the instance load time on subsequent restarts.

Then, scroll to the bottom of the page and click "Create". The page will redirect to the virtual machine list, and show the status of the machine starting up. 

After the machine starts, it can take up to 15 minutes for everything in the startup script to be installed. Wait 15 minutes or so, and then copy the External IP address. 

Open a browser. In the browser's location field, type `http://` and paste the IP address. It should end up looking like `http://34.125.96.234`. Then press `enter/return` to go to your Elpis machine. 

With Elpis going, follow the steps in the [Elpis workshop guide](elpis-workshop.md).


## Adding projects (optional)

Later, you may wish to add a new project to separate the usage of services across different experiments or activities. 

Click the project list in the top blue menu. In the popup, click "New Project".

On the New Project screen, add a project name and press "Create".

When the project has been created, you will be prompted to select it. Having done that, the page will show the project's Dashboard. 
