# Viewing Elpis training log file

During the training stage a log file is written to `/state/of_origin/models/XXXX/train.log`. Note that this file isn't created as soon as the `Start Training` button is clicked, there is a slight delay while some data prep is done. To view this file:


1. Connect to the VM if Elpis is running on a cloud machine. [Install gcloud](https://cloud.google.com/sdk/docs/install) if you don't have it already.

```shell
gcloud compute instances list
gcloud compute ssh instance-1
```

2. Run this command to get into the Elpis container.

```shell
docker exec -it elpis bash
```

3. Look in the `/state/of_origin/models` directory. The hashes are directories of the models that have been made. Change into the current model dir.

```shell
cd /state/of_origin/models
ls
cd <some_model_hash>
```

4. If `train.log` file is there, you can look at it for some insight into what Kaldi or HFT are doing. If Elpis is currently training, use `tail` to stream the log as it updates. 

```shell
tail -f train.log
```
