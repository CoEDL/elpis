# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Date is year-month-day format.

## [0.97.2] - 2021-12-23
### ADDED 
- Delete buttons for datasets, pron dicts and models
- Minor bug fixes

## [0.97.1] - 2021-12-08
### Changed 
- 44.1kHz sample rate to 16kHz

## [0.97.0] - 2021-12-05
### Added
- Huggingface Transformers wav2vec2 engine
### Changed
- Fixed CLI examples
### Removed 
- ESPnet engine

## [0.96.12] - 2021-11-10
### Added
- Automated docker builds on releases (vX.Y.Z) and pushes to master (latest)

## [0.96.11] - 2021-11-09
### Changed
- Change ports from 5000 to 5001 to avoid conflict with greedy MacOS Airplay speaker thing 

## [0.96.10] - 2021-10-28
### Changed
- Show Kaldi hypothesis confidence on the transcription page 

## [0.96.9] - 2021-08-27
### Changed
- Updated pympi, praatio, llvm, librosa, numba versions

## [0.96.7] - 2021-03-23
### Added
- Front end and dynamic i18n support

## [0.96.6] - 2021-03-6
### Changed
- Minor gui tweaks

## [0.96.5] - 2021-03-5
### Changed
- New flow for GUI welcome and engine select
- Start implementing feedback from UX study
- Show train logs in GUI. Kaldi is split into stages, ESPnet is single stage.
- Add DEV_MODE setting for GUI
- Pin ESPnet to CoEDL fork of persephone-tools/espnet

## [0.96.4] - 2021-03-4
### Changed
- Changed to use pyenv for Python version management

## [0.96.3] - 2021-01-26
### Changed
- Voice Activity Detection
- Bring GUI Dockerfile into line with with CPU version

## [0.96.2] - 2021-01-07
### Changed
- Modify Elpis to use Poetry for dependency management

## [0.96.1] - 2021-01-05
### Changed
- Dockerfile to use Python 3.8 as default for Elpis

## [0.96.0] - 2020-12-29
### Changed
- Monorepo: brought https://github.com/coedl/elpis-gui into this repo under elpis/gui
- Significant restructure: moved gpu and examples under /elpis
- Updated Docker image to an Ubuntu 20.04 base image

## [0.95.2] - 2020-12-08
### Changed
- Dockerfile to use Python 3.7 as default for Elpis


## [0.95.1] - 2020-09-23
### Changed
- Rearranged Dockerfile to group like things and install ESPne earlier


## [0.95.0] - 2020-09-20
### Added
- ESPnet

### Changed
- Fixed changelog date for docs


## [0.94.6] - 2020-09-07
### Added
- Docs

### Changed
- Separated log files into individual logs for each stage while processing, and build complete log when done
- Fixed annotations not resetting when changing tier settings
- Moved CLI example into a Kaldi dir
- Fixed Kaldi Elan CLI example, now links dataset and pronunciation dictionary independently
