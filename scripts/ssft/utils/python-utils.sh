#!/usr/bin/env bash

python_3_3() {
    if ( $VERBOSE ); then
        python3.3 $@
    else
        python3.3 $@ >> /dev/null
    fi
}

_check_first_arg(){
    if [ -z "$1" ]; then
        message_box "Please specify virtual env path for '$2' function"
        exit 1
    fi
}

python_virtualenv_create(){
    _check_first_arg "$1" "python_virtualenv_create"
    message_box "Setting up virtualenv using python3.3 into $1"
    if [ ! -d "$1" ]; then
        virtualenv --distribute -p `which python3.3` "$1"
        validate_operation_status "Failed to create virtual env by path: $1"
    fi
}


python_virtualenv_activate(){
    _check_first_arg "$1" "python_virtualenv_activate"
    echo "Activate virtual environment: $1"
    source "$1/bin/activate"
    validate_operation_status "Failed to activate $1"
    if ( $VERBOSE ); then
        python --version 2>&1 | xargs echo "Python env: "
        pip --version | xargs echo "pip env: "
    fi
}

python_virtualenv_deactivate(){
    echo "Deactivate virtual environment"
    deactivate
}

python_virtualenv_remove(){
    _check_first_arg "$1" "python_virtualenv_remove"
    rm_dir_if_exist "$1"
}

pip_3_3(){
    echo "Execute 'pip3.3 $@'"
    if ( $VERBOSE ); then
        pip3.3 $@
    else
        pip3.3 $@ >> /dev/null
    fi
}