# Viewing Elpis training log file

During the training stage a log file is written to /state/models/XXXX/train.log. Note that this file isn't created as soon as the Start Training button is clicked, there is a slight delay while some data prep is done. To view this file:


1. Run Elpis if it isn't already going.

```shell
docker run --rm -p 5001:5000/tcp coedl/elpis:latest
```


2. Open another terminal window and run this command to find the process ID of the elpis process. We'll use this to open another view into the same container.

```shell
docker ps
```

3. Should give results like:

```shell
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
b5d2ec4a5ea3        coedl/elpis:latest   "flask run --host 0.…"   3 minutes ago       Up 3 minutes        0.0.0.0:5001->5000/tcp   elastic_merkle
```


4. Use the CONTAINER ID number to interact with the container. Replace `CONTAINER_ID` in the following command with whatever yours is, and run it.

```shell
docker exec -it CONTAINER_ID bash
```


5. Or use this one-liner: `docker exec -it $(docker ps -q) bash`


6. Look in the `/state/models` directory. The hashes are directories of the models that have been made. Change into the current model dir. 
```shell
cd /state/models
ls
cd XXXX
```


7. If `train.log` file is there, you can look at it for some insight into what Kaldi is doing. We'll add some better feedback for knowing when this file is created soon.

```shell
tail -f train.log
```

For ESPnet, you will need to look in the egs dir for processing after stage 4. 
```shell
cd espnet-asr1/exp/train_nodev*
tail -f train.log
```