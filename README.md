# Elpis (Automatic Transcription for Linguists) <img src="docs/img/elpis.png" align="right" width="250px"/>

## What is Elpis?

Elpis is a tool which allows language workers with minimal computational experience to build their own speech models 
for use in automatically transcribing audio. It relies on the [Kaldi](http://kaldi-asr.org) automatic speech recognition 
(ASR) library. Kaldi is notorious for being difficult to build, use and navigate - even for trained computer scientists. 
The goal of Elpis is to expose the power of Kaldi to linguists and language workers by abstracting away much of the 
needless technical complexity.

Currently, the major component of Elpis is [kaldi_helpers](https://github.com/CoEDL/kaldi_helpers), a collection of 
Python and shell scripts designed to prepare data for use with Kaldi and convert between the various time-aligned 
transcription formats that linguists work with.

![Elpis Pathway](./docs/img/elpis-pipeline.svg)

## How Does It Work?

Elpis uses [Docker](https://www.docker.com/), specifically an [Ubuntu Linux](https://www.ubuntu.com/) image, to install
Kaldi and its (many) dependencies. It also installs [kaldi_helpers](https://github.com/CoEDL/kaldi_helpers) and the 
[Task](https://taskfile.org/#/) task runner. We have defined a number of tasks which automate many common workflows like
data preparation, model creation and inferring transcriptions for new files. You can read about these tasks and how to 
use them [here](https://github.com/CoEDL/elpis/wiki/tasks).

## How Do I Use It?

Please check the [wiki](https://github.com/CoEDL/elpis/wiki/Elpis-Step-By-Step-Guide) pages for a step-by-step guide to
using Elpis on your data. If you're comfortable using Docker and are aware of the types of data required, you can also 
consult our more concise 
[advanced guide](https://github.com/CoEDL/elpis/wiki/Inferring-Transcriptions-for-New-Audio-Data-(Advanced)).

## Why Is It Called Elpis?

Elpis was the ancient Greek goddess of hope. For us Elpis represents our hope that one day everyone will have access to 
the power of ASR without having to interact directly with the [Kaldi codebase](https://github.com/kaldi-asr/kaldi).
We've also backronymed it to stand for "Endangered Language Pipeline and Inference System," as much of our motivation 
for this project derives from our desire to assist in documentation and revitalisation efforts for the world's many
endangered languages - including many in Australia, where most of Elpis' development has occurred.

## I'm An Academic, How Do I Cite This?

This software is the product of academic research funded by the Australian Research Council 
[Centre of Excellence for the Dynamics of Language](http://www.dynamicsoflanguage.edu.au/). If you use the software 
or code in an academic setting, please be sure to cite it appropriately as follows:
> Foley, B., Arnold, J., Coto-Solano, R., Durantin, G., Ellison, T.M., van Esch, D., Heath, S., Kratochvíl, F., Maxwell-Smith, Z., Nash, D. and Olsson, O., 2018. Building Speech Recognition Systems for Language Documentation: The CoEDL Endangered Language Pipeline and Inference System (ELPIS).

