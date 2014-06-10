#!/bin/sh

# check local celeryd-edextract serives by ps
readonly PROGNAME=$(basename $0)

CMD="ps -f -U root -u root|grep filerouter.filerouter 2> /dev/null"

usage() {
    echo "  usage: ${PROGNAME}"
    echo ""
    echo "      nagios plugin that checks file router services is running."
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
            echo "FILE ROUTER OK"
            exit 0
        else
            echo "FILE ROUTER CRITICAL"
            exit 2
        fi
     else
        echo "FILE ROUTER UNKNOWN"
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