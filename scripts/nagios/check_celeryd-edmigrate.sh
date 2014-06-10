#!/bin/sh

# check local celeryd-edmigrate serives by ps
readonly PROGNAME=$(basename $0)

CMD="ps -f -U celery -u celery|grep edmigrate.edmigrate_celery 2> /dev/null"

usage() {
    echo "  usage: ${PROGNAME}"
    echo ""
    echo "      nagios plugin that checks celeryd-edmigrate services is running."
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
            echo "CELERYD-EDMIGRATE OK"
            exit 0
        else
            echo "CELERYD-EDMIGRATE CRITICAL"
            exit 2
        fi
     else
        echo "CELERYD-EDMIGRATE UNKNOWN"
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