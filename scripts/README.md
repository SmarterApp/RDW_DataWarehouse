Scripts
=======

We store that start, stop, initialize server. Or development machine set up scripts here


# ssft
ssft (single setup for testing) contains scripts that allow to prepare environment for unit and/or automation testing.
ssft folder contains 3 main scripts:
- build.sh - responsible for virtual environment creation, DB set up, ini configuration
- manage.sh - responsible for run, stop of some application used in SRL
- test.sh - responsicle for run of unit and/or automation tests

To get more details about parameters, just call reqired script without parameters.

## UDL specific settings
gpg keys have to be located by the next scheme:
 - stating keys: ~/.gnupg/staging
 - local keys: ~/.gnupg/local