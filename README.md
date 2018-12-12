# Elpis

Elpis is a pipeline of tools which language documentation workers with minimal computational experience can use to build their own speech models, using the Kaldi automatic speech recognition system.

The code is currently over at https://github.com/CoEDL/kaldi-helpers but will be moving here soon.

## Summer School 2018 workshop

Please check the [wiki](https://github.com/CoEDL/elpis/wiki) pages for workshop steps.

## Project Structure

This repository is a full stack server to build a friendly interface for the Kaldi tool set. Flask is the backend of choice while the front-end is composed of React and other Javascript libraries that are bundled together.

### Setup

TODO
```bash
$ npm i
```

### Deployment

Before running the server, the Javascript, React and CSS code needs to be bundled for deployment. To do this, run:

```basb
$ webpack
```

The above command takes the Javascript, React and CSS code from the elpis/web/ directory and places it in the template and static folders.

To run the flask server, type in command-line:

```bash
$ python elpis
```