# Docker commands

The following commands can be executed in the **Terminal** (in Linux or MAC systems) or in the **Command Prompt** (in Windows systems), for managing Docker containers.

1. List the images that you have.
```
# docker images
```


2. Remove images.
```
# docker image prune -a
```
Verify that the images have been removed by running `docker images` again.


If the images are still there, you may need to remove stopped containers first, then re-run image prune.
```
# docker container prune
```


3. Save an image to USB. This command enables compressing the docker image as a tar file and saving it.
```
# docker save alpine > /path_to_the_usb_location/alpine.tar
```


4. Load a docker image from disk, after *cd* to where the image file is located
```
cd /path_to_the_usb_location/alpine.tar
docker load -input alpine.tar
```
