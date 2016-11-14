#!/bin/bash

set -e  # Exit on errors

# connect dependencies
_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$_DIR/constants.sh"
source "$_DIR/utils/bash-utils.sh"
source "$_DIR/utils/python-utils.sh"
source "$_DIR/utils/process-utils.sh"


# options to execute
SMARTER=false
HPZ=false
TSB=false
UDL=false
EDMIGRATE=false
PREPDF=false
ALL=false

# specific
EDMIGRATE_UDL=false
EDMIGRATE_PR=false
FILES=false

RUN=false
STOP=false
VERIFY=false
WATCH=false
REMOVE_LOG_FILE=false

VERBOSE=false

_usage(){
    echo "Usage:
    ./`basename $0` command application                     ./`basename $0` run smarter
    ./`basename $0` command application application         ./`basename $0` run -s -h
    ./`basename $0` command application sub-command         ./`basename $0` run edmigrate --udl-migration
    ./`basename $0` command application flag                ./`basename $0` run -s --verbose

Commands:
    run                                                 run specified application
    stop                                                stop specified application
    verify                                              display PID's info
    watch                                               tail logs for specified applications

Applications:
    -m, edmigrate
    -h, hpz
    -s, smarter
    -t, tsb
    -u, udl
    -p, prepdf-generator
    all

Sub-commands
    applicable only with 'run' command:
        edmigrate application:
            --mu, --udl-migration
            --mp, --public-reports-migration
        UDL application:
            --files, --process-files-through-udl        run procession of .json and .csv through UDL
            --                                          separate parameters for '--files' sub-command
    applicable only with 'watch' command:
        --from-now                                      remove previous log file

Flags:
    --verbose                                           show more logs
    " && list_variables

}

_read_options(){
    if [ -z "$1" ]; then
        _usage
        exit $E_OPTERROR;
    fi

    while true; do
        case "$1" in
            -m | edmigrate)                              EDMIGRATE=true;       shift ;;
            -h | hpz)                                    HPZ=true;             shift ;;
            -s | smarter)                                SMARTER=true;         shift ;;
            -t | tsb)                                    TSB=true;             shift ;;
            -u | udl)                                    UDL=true;             shift ;;
            -p | prepdf)                                 PREPDF=true;          shift ;;
            all)                                         ALL=true;             shift ;;
            --mu | --udl-migration)                      EDMIGRATE_UDL=true;   shift ;;
            --mp | --public-reports-migration)           EDMIGRATE_PR=true;    shift ;;
            run)                                         RUN=true;             shift ;;
            stop)                                        STOP=true;            shift ;;
            verify)                                      VERIFY=true;          shift ;;
            watch)                                       WATCH=true;           shift ;;
            --files | --process-files-trough-udl)        FILES=true;           shift ;;
            --from-now)                                  REMOVE_LOG_FILE=true; shift ;;
            --) shift;
                if [ -n "$1" ]; then EDWARE_UDL_MODE="$1"; shift; fi
                if [ -n "$1" ]; then EDWARE_UDL_ARCHIVE_PREFIX="$1"; shift; fi
                if [ -n "$1" ]; then EDWARE_UDL_FILES="$@"; fi
                break ;;
            --verbose)                                   VERBOSE=true;        shift ;;
            '') break ;;
            *) echo "Unsupported option: '$1'"; _usage; exit -1 ;;
        esac
    done
}

_run_app(){
    if [ -n "$1" -a -n "$2" ]; then
        if ( $RUN ); then
            python_virtualenv_activate "$2"
        fi
        (
        source "$_DIR/$1"
        set -e
        if ( $RUN ); then
            message_box "Run '$1', python env: '$2'"
            if ( $EDMIGRATE_UDL ); then __run_udl_migration;
            elif ( $EDMIGRATE_PR ); then __run_public_reports;
            elif ( $FILES ); then __process_files;
            else __run; fi
        elif ( $STOP ); then
            message_box "Stop '$1', python env: '$2'"
            __stop
        elif ( $VERIFY ); then
            message_box "Verify '$1', python env: '$2'"
            __verify
        else
            message_box "Nothing selected"
            exit -10
        fi
        ) || echo "Warning: unable to execute a command for '$1'"
        if ( $RUN ); then
            python_virtualenv_deactivate
        fi
    else
        echo "Above params are incorrect"
    fi
}

_run_watch(){
    log_files=()
    if ( $ALL || $SMARTER );    then log_files+=($EDWARE_LOG_SMARTER);      fi
    if ( $ALL || $HPZ );        then log_files+=($EDWARE_LOG_HPZ);          fi
    if ( $ALL || $TSB );        then log_files+=($EDWARE_LOG_TSB);          fi
    if ( $ALL || $UDL );        then log_files+=($EDWARE_LOG_UDL);          fi
    if ( $ALL || $PREPDF );     then log_files+=($EDWARE_LOG_PREPDF);       fi
    if ( $ALL || $EDMIGRATE );  then log_files+=($EDWARE_LOG_EDMIGRATE);    fi
    if ( $REMOVE_LOG_FILE ); then
        rm -rf ${log_files[@]}
        touch ${log_files[@]}
    fi
    tail -F ${log_files[@]}
}

_main(){
    _read_options $@
    if ! ( $RUN || $STOP || $VERIFY || $WATCH); then
        message_box "Please specify a command"
        _usage
        exit -10;
    fi
    if ( $WATCH ); then
        _run_watch
    fi
    if ( $RUN && ! $EDMIGRATE_UDL && ! $EDMIGRATE_PR && ! $FILES ); then
        mkdir -p $EDWARE_LOG_HOME
        _run_app "apps/services.sh" "$EDWARE_VENV_SMARTER"
    fi

    if ( $SMARTER || $ALL ); then
        _run_app "apps/smarter.sh" "$EDWARE_VENV_SMARTER"
    fi
    if ( $EDMIGRATE && $RUN ); then
        _run_app "apps/edmigrate.sh" "$EDWARE_VENV_EDMIGRATE"
    fi
    if ( $HPZ || $ALL ); then
        _run_app "apps/hpz.sh" "$EDWARE_VENV_HPZ"
    fi
    if ( $TSB || $ALL ); then
        _run_app "apps/tsb.sh" "$EDWARE_VENV_TSB"
    fi
    if ( $UDL || $ALL ); then
        _run_app "apps/udl.sh" "$EDWARE_VENV_UDL"
    fi
    if ( $PREPDF && $RUN ); then
        _run_app "apps/prepdf_generator.sh" "$EDWARE_VENV_SMARTER"
    fi
    exit 0
}

_main $@
exit -10
