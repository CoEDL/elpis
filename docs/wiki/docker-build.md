# Building the Elpis Docker image

To build an image locally, use this command.
```
docker build --tag IMAGE_NAME .
```

For example,
```
docker build --tag coedl/elpis:latest --tag coedl/elpis:0.96.8 .
```

After building, push to the hub.
```
docker push coedl/elpis:latest
docker push coedl/elpis:0.96.8
```

Or push all tags.
```
docker image push --all-tags coedl/elpis
```


## Build issues

Docker build issues  may be due to Docker storage being full. This may be indicated by error messages such as:
```
E: The repository 'http://archive.ubuntu.com/ubuntu focal-updates InRelease' is not signed.
W: GPG error: http://archive.ubuntu.com/ubuntu focal-backports InRelease: At least one invalid signature was encountered.
```

Try cleaning space with these commands, and then rebuild.
```
docker image prune
docker container prune
docker builder prune
```
