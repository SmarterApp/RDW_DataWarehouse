#!/bin/sh

# use virtualenv to run initialization script
source ~/py33/bin/activate

python -m udl2.database $1 $2 $3 $4
