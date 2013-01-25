#!/bin/bash

set -e # Exit on errors

function check_vars {

    # This is really just to make sure that we're running this on Jenkins
    if [ -z "$WORKSPACE" ]; then
        echo "\$WORKSPACE is not defined"
        exit 2
    fi
    if [ ! -d "$WORKSPACE" ]; then
        echo "WORKSPACE: '$WORKSPACE' not found"
        exit 2
    fi
}

function set_vars {
    # We probably don't want this hardcoded to python3
    export PATH="/usr/local/bin/:$PATH"

    export VIRTUALENV_DIR="$WORKSPACE/edwaretest_venv"
}

function setup_virtualenv {
    echo "Setting up virtualenv"
    if [ ! -d "$VIRTUALENV_DIR" ]; then
        /usr/local/bin/virtualenv --no-site-packages ${VIRTUALENV_DIR}
    fi

# This will change your $PATH to point to the virtualenv bin/ directory,
# to find python, paster, nosetests, pep8, pip, easy_install, etc.
    
    source ${VIRTUALENV_DIR}/bin/activate
    
    cd "$WORKSPACE/$1"
    python setup.py develop

    # Setup test dependencies
    # Need to figure out how to run test with nosetest 
    #python setup.py test
    pip install nose
    pip install coverage

    echo "Finished setting up virtualenv"
}

function check_pep8 {
    echo "Checking code style against pep8"
    $WORKSPACE/bin/linters/pep8.sh
    echo "Finished checking code style against pep8"
}

function run_unit_tests {
    echo "Running unit tests"

    cd "$WORKSPACE/$1"
    nosetests -v --with-coverage --cover-package=$1  --with-xunit --xunit-file=$WORKSPACE/nosetests.xml
}

function main {
    check_vars
    set_vars
    setup_virtualenv $1
    run_unit_tests $1
    #check_pep8
}

main $1

# Completed successfully
exit 0
