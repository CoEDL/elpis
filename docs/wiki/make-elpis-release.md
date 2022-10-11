# Making a release

Follow these steps to make a release and new Docker image for Elpis. 


## Update version in the code

Update the changelog and version details in the Elpis repo.

```
~/sandbox/elpis/CHANGELOG.md
~/sandbox/elpis/pyproject.toml
~/sandbox/elpis/docs/conf.py
~/sandbox/elpis/elpis/gui/package.json
```

## Docs

Update docs if required with any description of changed functionality. Pushing to master will rebuild the readthedocs repo.


## Try the code

Test GUI build as a sanity check that the app builds and eslint is happy. You may need to set your local Node to the version required for the GUI. These commands use *asdf* to manage Node version. Information about installing and using *asdf* are [here](https://asdf-vm.com/).

```
cd ~/sandbox/elpis/elpis/gui
asdf local nodejs 15.14.0
yarn install && yarn build
```


Build a new Docker image.

```
cd ~/sandbox/elpis
docker build --tag elpis-latest-test .
```


Check that app runs with the new image. This isn't mounting any local repos in so it's a good way to check that the image is self-contained. 

```
docker run --rm -p 5001:5001/tcp elpis-latest-test
```

Open `http://0.0.0.0:5001` in a browser, and do train and test with at least a [toy corpus](https://github.com/CoEDL/toy-corpora). For Kaldi, use the Abui toy corpus. The Na toy corpus may be more suitable for checking the HFT engine.

If it's all good, retag the image with the coedl org and push it to the Docker Hub

```
docker login
docker tag elpis-latest-test coedl/elpis:latest
docker tag elpis-latest-test coedl/elpis:0.xx.xx
docker push coedl/elpis:latest 
docker push coedl/elpis:0.xx.xx
```


You can push all tags with this command. But don't do this if you have random dev tags.

```
docker push coedl/elpis
```


Clean up Docker

```
docker image rm elpis-latest-test
docker image prune -a
```


## Push Git version commit

Push a commit for the version bump.


## Make a Git release

* Draft a [new release](https://github.com/CoEDL/elpis/releases/new)
* Click `Choose a tag` and type the next version num including a leading `v`. E.g. `v0.96.10`
*  Select `+ Create new tag: xxx on publish` to save the tag when the release is published.
* Leave release title empty to use the tag as the title.
* Write a description of the release (should be the same as the changelog info).
* Click `Publish release`. This will bundle the code as `.zip` and `.tar.gz` assets with the release.

done
