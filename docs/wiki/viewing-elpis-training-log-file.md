# Viewing Elpis training log file

**TODO: update paths for v0.94, the log is now in `/state/model/HASH/run_log.txt`**

During the training stage a log file is written to /elpis/state/tmp_log.txt. Note that this file isn't created as soon as the Start Training button is clicked, there is a slight delay while some data prep is done. To view this file:


1. Run Elpis if it isn't already going.

```
docker run --rm -p 5000:5000/tcp coedl/elpis:latest
```


2. Open another terminal window and run this command to find the process ID of the elpis process. We'll use this to open another view into the same container.

```
docker ps
```

3. Should give results like:

```
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
b5d2ec4a5ea3        coedl/elpis:online   "flask run --host 0.…"   3 minutes ago       Up 3 minutes        0.0.0.0:5000->5000/tcp   elastic_merkle
```


4. Use the CONTAINER ID number to interact with the container. Replace `CONTAINER_ID` in the following command with whatever yours is, and run it.

```
docker exec -it CONTAINER_ID bash
```


5. Or use this one-liner: `docker exec -it $(docker ps -q) bash`


6. Look at the files in the `/elpis/state` directory. 
```
ls /elpis/state
```


7. If `tmp_log.txt` file is there, you can look at it for some insight into what Kaldi is doing. We'll add some better feedback for knowing when this file is created soon.

```
tail -f /elpis/state/tmp_log.txt
```

There are stages during training which even this file appears to not give progress updates, particularly during the stage when the mfcc audio features are being generated.
