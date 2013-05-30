#!/bin/bash

set -e

# This is really just to make sure that we're running this on Jenkins
if [ -z "$WORKSPACE" ]; then
    echo "\$WORKSPACE is not defined"
    exit 2
fi
if [ ! -d "$WORKSPACE" ]; then
    echo "WORKSPACE: '$WORKSPACE' not found"
    exit 2
fi

VIRTUALENV_DIR="$WORKSPACE/ansible_venv"

echo "Setting up virutalenv using python2.6"

if [ ! -d "$VIRTUALENV_DIR" ]; then
    virtualenv -p /usr/bin/python2.6 --distribute ${VIRTUALENV_DIR}
fi

source ${VIRTUALENV_DIR}/bin/activate

echo "Installing ansible"
pip install ansible

echo "Finished installing ansible"

echo "Finished setting up environment"
