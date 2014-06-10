#!/bin/sh

# check local celeryd-edextract serives by ps
readonly PROGNAME=$(basename $0)

CMD="ps -f -U celery -u celery|grep repmgrd-watcher 2> /dev/null"

usage() {
    echo "  usage: ${PROGNAME}"
    echo ""
    echo "      nagios plugin that checks REPMGRD-WATCHER services is running."
    echo "      the plugin returns status 0 when service is running."
    echo "      returns status 2 when service has an internal error."
    echo "      returns status 3 when service is not reachable"
}

probe() {
     IFS=$'\n'
     local OUTPUT=`eval $CMD`
     if [[ $? == '0' ]]
     then
        if [[ ! -z $OUTPUT ]]
        then
            echo "REPMGRD-WATCHER OK"
            exit 0
        else
            echo "REPMGRD-WATCHER CRITICAL"
            exit 2
        fi
     else
        echo "REPMGRD-WATCHER UNKNOWN"
        exit 3
     fi

}


main() {
    if [[ ! -z "${ARGS}" ]]
    then
        usage
    else
        probe
    fi
}
main