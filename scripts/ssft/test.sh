#!/usr/bin/env bash

set -e # Exit on errors

# connect dependencies
_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$_DIR/constants.sh"
source "$_DIR/utils/bash-utils.sh"
source "$_DIR/utils/python-utils.sh"

DEFAULT_UNIT_MODULES=(
    config
    data_gen
    edapi
    edauth
    edcore
    edextract
    edmigrate
    edschema
    edsftp
    edudl2
    edworker
    hpz
    hpz_client
    integration_tests
    services
    smarter
    smarter_common
    smarter_score_batcher
)

DEFAULT_AUTOMATION_MODULES=(
    edware_testing_automation
)

UNIT=false
AUTOMATION=false
ALL=false
REPORT=false

UNIT_MODULES=()
AUTOMATION_MODULES=()

VERBOSE=false

ALLURE_DIR="allure-report"
ALLURE_ERRORS="allure.errors"

_usage(){
    echo "Usage:
    ./`basename $0` tests                   ./`basename $0` unit-tests
    ./`basename $0` tests module module     ./`basename $0` -u -um edapi -a -am edware_testing_automation/edapi_tests/test_get.py
    ./`basename $0` tests module flag       ./`basename $0` all --report --verbose

Tests:
    -u, unit-tests
    -a, automation-tests
    all

Options:
    -um, --unit-tests-module
    -am, --automation-tests-module

Flags:
    --report                            generate and open Allure report
    --verbose                           show more logs
    " && list_variables
}

_read_options(){
    if [ -z "$1" ]; then
        _usage
        exit $E_OPTERROR;
    fi

    while true; do
        case "$1" in
            -u | unit-tests)                 UNIT=true;                         shift ;;
            -um | --unit-tests-module)       shift; UNIT_MODULES+=("$1");       shift ;;
            -a | automation-tests)           AUTOMATION=true;                   shift ;;
            -am | --automation-tests-module) shift; AUTOMATION_MODULES+=("$1"); shift ;;
            all)                             ALL=true;                          shift ;;
            --report)                        REPORT=true;                       shift ;;
            --verbose)                       VERBOSE=true;                      shift ;;
            '') break ;;
            *) echo "Unsupported option: '$1'"; _usage; exit -1 ;;
        esac
    done
}

_check_pep8(){
    echo "********************************"
    echo "Checking code style against pep8"
    echo "********************************"
    ignore="E501,E265,E402"

    pep8 --ignore=$ignore "$EDWARE_WORKSPACE/$1"

    echo "Finished checking code style against pep8"
}

_run_unit_tests(){
    message_box "Running unit tests"
    python_virtualenv_activate "$EDWARE_VENV_BASKET"
    cd "$EDWARE_WORKSPACE"

    for module in $@; do
        message_box "Run tests for '$module' module"
        cd "$module"
        (
            if ( $VERBOSE ); then
                nosetests --with-allure --logdir=$ALLURE_DIR
            else
                nosetests -q --with-allure --logdir=$ALLURE_DIR >> /dev/null
            fi
        ) || echo "Some unit tests are failed."
        cd ..
    done
    python_virtualenv_deactivate

}

_run_automation_tests(){
    message_box "Running automation tests"
    python_virtualenv_activate "$EDWARE_VENV_TESTS"
    cd "$EDWARE_WORKSPACE/tests"
    (
        if ( $VERBOSE ); then
            py.test --alluredir=$ALLURE_DIR $@
        else
            py.test -q --alluredir=$ALLURE_DIR $@ >> /dev/null
        fi
    ) || echo "Some automation tests are failed."
    cd ..
    python_virtualenv_deactivate
}

_combine_allure_reports() {
    message_box "Combine reports into $EDWARE_WORKSPACE/$ALLURE_DIR"
    mkdir -p "$EDWARE_WORKSPACE/$ALLURE_DIR"
    for module in $@; do
        echo "Copy reports for '$module' module"
        if [ -d $EDWARE_WORKSPACE/$module/$ALLURE_DIR/ ]; then
            (cp -r $EDWARE_WORKSPACE/$module/$ALLURE_DIR/* $EDWARE_WORKSPACE/$ALLURE_DIR/) || echo "
        Warning! '$module' module.
        '$EDWARE_WORKSPACE/$module/$ALLURE_DIR/' folder doesn't have XML file(s) for allure.
            " >> $ALLURE_ERRORS
        else
            echo "
        Error: Unable to find allure results for '$module' module.
        Invalid path: $EDWARE_WORKSPACE/$module/$ALLURE_DIR/
            " >> $ALLURE_ERRORS
        fi
    done
}

_generate_allure_report(){
    if [ -f $ALLURE_ERRORS ]; then
        message_box "There are some errors during copying of allure result to '$EDWARE_WORKSPACE/$ALLURE_DI'"
        cat $ALLURE_ERRORS
    fi
    message_box "Generate report from $EDWARE_WORKSPACE/$ALLURE_DIR"
    allure generate --report-dir "$EDWARE_WORKSPACE/$ALLURE_DIR" "$EDWARE_WORKSPACE/$ALLURE_DIR"
    allure report open --report-dir "$EDWARE_WORKSPACE/$ALLURE_DIR"

}
_clean_up(){
    rm_dir_if_exist "$EDWARE_WORKSPACE/$ALLURE_DIR"
    rm_file_if_exist $ALLURE_ERRORS
    rm -rf /opt/edware/zones/landing/history/*
    rm -rf /opt/edware/zones/landing/work/*
}

main(){
    _read_options $@
    _clean_up
    if ( $ALL || $UNIT ); then
        if [ ${#UNIT_MODULES[@]} -eq 0 ]; then
            _run_unit_tests ${DEFAULT_UNIT_MODULES[@]}
            _combine_allure_reports ${DEFAULT_UNIT_MODULES[@]}
        else
            _run_unit_tests ${UNIT_MODULES[@]}
            _combine_allure_reports ${UNIT_MODULES[@]}
        fi
    fi
    if ( $ALL || $AUTOMATION ); then
        if [ ${#AUTOMATION_MODULES[@]} -eq 0 ]; then
            _run_automation_tests ${DEFAULT_AUTOMATION_MODULES[@]}
            _combine_allure_reports tests
        else
            _run_automation_tests ${AUTOMATION_MODULES[@]}
            _combine_allure_reports tests
        fi
    fi
    if ( $REPORT ); then
        _generate_allure_report
    fi
}

main $@
