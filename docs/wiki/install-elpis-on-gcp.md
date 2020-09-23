# Installing Elpis on Google Cloud Platform

Create an account at Google Cloud https://cloud.google.com/

Here's a [quickstart quide](https://cloud.google.com/compute/docs/quickstart-linux) to getting a machine running.

The smallest vCPU instance on GCP is more than enough for the toy data set. That's g1-small (Shared-core machine type with 0.5 vCPU, 1.70 GB of memory, backed by a shared physical core). At training time CPU usage peaks at about 10% of the available compute on that instance type. For a bigger data set, choose a faster machine.

In the `management options` section, paste the script from below. Keep an eye on the Elpis wiki for information about the latest version of Elpis.

```
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
curl -O https://download.docker.com/linux/ubuntu/dists/bionic/pool/edge/amd64/containerd.io_1.2.2-3_amd64.deb
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
sudo apt install ./containerd.io_1.2.2-3_amd64.deb
sudo apt install -y docker-ce
sudo docker run -d --rm -p 80:5000/tcp coedl/elpis:interspeech-19

```