# Install Elpis on Google Cloud for Kaldi

If this is your first time using Elpis on Google Cloud, follow the steps on the [Setup Google Cloud account](setup-google-cloud-account.md) page. 


## Create a Virtual Machine 

Go to the `Compute Engine > VM Instances` page.

Click "Create"

+ Name it
+ Select a Region and Zone
+ Choose a machine size. The size will determine how much it will cost to run. The smallest vCPU instance on GCP is more than enough for the toy data set. That's first series N1 with g1-small (shared-core machine type with 0.5 vCPU, 1.70 GB of memory, backed by a shared physical core). At training time CPU usage peaks at about 10% of the available compute on that instance type. For a bigger data set, or for faster training & transcription time, choose a faster machine.

+ Increase the boot disk size to 20GB plus the size of your training corpus. For example, to train with 5GB of audio and ELAN files, set the disk size to 25GB. 
+ Select HTTP and HTTPS traffic in the Firewall options
+ Click the "Management, security, disks, networking, sole tenancy" link. 

Paste the following code into the "Startup Script" box

```
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce
sudo chmod 666 /var/run/docker.sock
mkdir /state
sudo docker run -d --name elpis -v /state:/state -p 80:5001/tcp coedl/elpis:latest
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
