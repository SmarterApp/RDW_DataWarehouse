#!/bin/bash

set -e  # Exit on errors

# connect dependencies
_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$_DIR/constants.sh"
source "$_DIR/utils/bash-utils.sh"
source "$_DIR/utils/python-utils.sh"
source "$_DIR/utils/srl-utils.sh"

# options to execute
SMARTER=false
HPZ=false
TSB=false
UDL=false
EDMIGRATE=false
BASKET=false
TESTS=false

ALL=false
CLEAN=false

VERBOSE=false

INCLUDE_DB=true
INCLUDE_INI=true
INCLUDE_DEPENDENCIES=true

_usage(){
    echo "Usage:
    ./`basename $0` application                 ./`basename $0` smarter
    ./`basename $0` application application     ./`basename $0` -s -h
    ./`basename $0` application flag            ./`basename $0` all --hard

Applications:
    -m, edmigrate                             please note that smarter has to be built first
    -h, hpz
    -s, smarter
    -t, tsb
    -u, udl                                   please build smarter before
    -b, all-into-basket                       unit tests env
    -a, automation-tests
    all

Flags:
    --without-db                              skip database set up
    --without-ini                             skip ini set up
    --without-packages                        skip code re-deploy
    --hard                                    re-create Python environment
    --verbose                                 show more logs
    " && list_variables

}

_read_options(){
    if [ -z "$1" ]; then
        _usage
        exit $E_OPTERROR;
    fi

    while true; do
        case "$1" in
            -m | edmigrate)           EDMIGRATE=true;                 shift ;;
            -h | hpz)                 HPZ=true;                       shift ;;
            -s | smarter)             SMARTER=true;                   shift ;;
            -t | tsb)                 TSB=true;                       shift ;;
            -u | udl)                 UDL=true;                       shift ;;
            all)                      ALL=true;                       shift ;;
            -b | all-into-basket)     BASKET=true;                    shift ;;
            -a | automation-tests)    TESTS=true;                     shift ;;
            --without-db)             INCLUDE_DB=false;               shift ;;
            --without-ini)            INCLUDE_INI=false;              shift ;;
            --without-packages)       INCLUDE_DEPENDENCIES=false;     shift ;;
            --hard)                   CLEAN=true;                     shift ;;
            --verbose)                VERBOSE=true;                   shift ;;
            '')                                                       break ;;
            *) echo "Unsupported option: '$1'"; _usage; exit -1 ;;
        esac
    done
}

_configure_app(){
    message_box "Configure app: script: '$1', python env: '$2'"
    if [ -n "$1" -a -n "$2" ]; then
        (
            message_box "Configure Python"
            if ( $CLEAN ); then
                python_virtualenv_remove "$2"
            fi
            python_virtualenv_create "$2"
            python_virtualenv_activate "$2"

            source "$_DIR/$1"

            if ( $INCLUDE_DEPENDENCIES ); then
                __dependencies
                validate_operation_status "Python's dependencies"
            fi
            if ( $INCLUDE_INI ); then
                __ini
                validate_operation_status "INI file set up"
            fi
            if ( $INCLUDE_DB ); then
                __db
                validate_operation_status "DB set up"
            fi

            python_virtualenv_deactivate

#            pip_3_3 uninstall -y -q WebOb
#            pip_3_3 install -q WebOb==1.5.1

        )
        validate_operation_status "Unable to build and configure '$1'"
    else
        echo "Above params are incorrect"
    fi
}

_main(){
    _read_options $@
    mkdir -p "$EDWARE_VENV_HOME"

    if ( $SMARTER || $ALL ); then
        _configure_app "apps/smarter.sh" "$EDWARE_VENV_SMARTER"
    fi
    if ( $EDMIGRATE || $ALL ); then
        _configure_app "apps/edmigrate.sh" "$EDWARE_VENV_EDMIGRATE"
    fi
    if ( $HPZ || $ALL ); then
        _configure_app "apps/hpz.sh" "$EDWARE_VENV_HPZ"
    fi
    if ( $TSB || $ALL ); then
        _configure_app "apps/tsb.sh" "$EDWARE_VENV_TSB"
    fi
    if ( $UDL || $ALL ); then
        _configure_app "apps/udl.sh" "$EDWARE_VENV_UDL"
    fi
    if ( $BASKET || $ALL ); then
        _configure_app "apps/basket.sh" "$EDWARE_VENV_BASKET"
    fi
    if ( $TESTS || $ALL ); then
        _configure_app "apps/tests.sh" "$EDWARE_VENV_TESTS"
    fi
    message_box "Commands executed successfully! Congratulations!!!"
    exit 0
}

_main $@
exit -10
