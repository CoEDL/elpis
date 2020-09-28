# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Date is year-month-day format.


## [0.95.1] - 2020-09-23
### Changed
- Rearranged Dockerfile to group like things and install ESPnet earlier


## [0.95.0] - 2020-09-20
### Added
- ESPnet

### Changed
- Fixed changelog date for docs


## [0.94.6] - 2020-09-07
### Added
- Docs

### Changed
- Separated log files into individual logs for each stage while processing, and build complete log when done.
- Fixed annotations not resetting when changing tier settings.
- Moved CLI example into a Kaldi dir
- Fixed Kaldi Elan CLI example, now links dataset and pronunciation dictionary independently
