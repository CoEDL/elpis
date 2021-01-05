# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Date is year-month-day format.

## [0.96.0] - 2020-12-29
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
