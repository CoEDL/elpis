# Install Elpis on Google Cloud for Kaldi


## Setup your account

Create an account at [Google Cloud](https://cloud.google.com).

When you have signed in, go to the [Getting Started](https://console.cloud.google.com/getting-started) page. Set your country and agree to the Terms of Service, then press "Agree and Continue".

You should land on the Console Home screen.

Make a new project using the CREATE PROJECT link. Later, you can create new projects from the "Select a Project" option in the blue top bar.

On the New Project screen, add a Project Name and press "Create".

When the project has been created, the console will show the project's Dashboard. 

To add a server to the project, open the left side Navigation Menu and select "Compute Engine". Then select "VM Instances". If this is the first time your Google account has used Cloud Platform you may be offered a free trial! If so, go through the process of signing up for it. Otherwise, you may need to add billing details to access VM instances (TODO add more info about that). You will need to enter credit card details during the free trial opt-in process, but you won't be billed unless you turn on Automatic Billing.


## Create a Virtual Machine 

Now that your account has free trial or billing set up, the VM instances page should show "Create" and "Import" buttons.

Click "Create"

+ Name it
+ Select a Region and Zone
+ Choose a machine size. The size will determine how much it will cost to run. The smallest vCPU instance on GCP is more than enough for the toy data set. That's first series N1 with g1-small (shared-core machine type with 0.5 vCPU, 1.70 GB of memory, backed by a shared physical core). At training time CPU usage peaks at about 10% of the available compute on that instance type. For a bigger data set, or for faster training & transcription time, choose a faster machine.

+ Increase the boot disk size to 20GB plus the size of your training corpus. For example, to train with 5GB of audio and ELAN files, set the disk size to 25GB. 
+ Select HTTP and HTTPS traffic in the Firewall options
+ Click the "Management, security, disks, networking, sole tenancy" link. 

Paste the following code into the "Startup Script" box

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

Then press "Create"

It will take between 15 to 30 minutes for the machine to start up and install all the software. 


## For multiple machines

Make an instance template with the same settings.

Install [gcloud](https://cloud.google.com/sdk/docs/install)

Create multiple machines with this command. Replace the zone and template values. Size is the number of instances.
```shell
gcloud compute instance-groups managed create elpis-group \
  --zone "us-central1-a" \
  --template "elpis-medium-template" \
  --size 2
  ```


## To inspect logs on GCP instances

Get their details (name, IP address)
```shell
gcloud compute instances list
```

SSH to an instance
```shell
gcloud compute ssh --project "elpis-workshop" --zone "us-central1-a" "elpis-group-p9t1"
```

Check if the image has started yet
```shell
docker ps
```

Interact and view logs etc (may not need sudo)
```shell
sudo docker exec -it $(sudo docker ps -q) bash
```

[See notes for accessing logs.](viewing-elpis-training-log-file.md)
