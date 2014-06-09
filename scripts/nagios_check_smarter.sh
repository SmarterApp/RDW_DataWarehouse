#!/bin/sh

# check local smarter services server by hitting host:port/services/heartbeat
readonly PROGNAME=$(basename $0)
readonly ARGS="$@"

if [[ ! -z $1 ]]
then
    readonly HOST=$1
else
    readonly HOST=""
fi

if [[ ! -z $2 ]]
then
    readonly PORT=$2
else
    readonly PORT=""
fi

WGET="wget -S --tries=1 --timeout=1 -q -O /dev/null http://$HOST:$PORT/services/heartbeat 2>&1 -"

usage() {
    echo "  usage: $PROGNAME hostname port"
    echo ""
    echo "      nagios plugin that checks smarter services is running."
    echo "      the plugin returns status 0 when service is running."
    echo "      returns status 2 when service has an internal error."
    echo "      returns status 3 when service is not reachable"
}

probe() {
     IFS=$'\n'
     local OUTPUT=`eval $WGET`
     if [[ $? == '0' ]]
     then
         local HAS_HTTP_200=`echo $OUTPUT |grep "HTTP/1.1 200 "`
        if [[ ! -z $HAS_HTTP_200 ]]
        then
            echo "SMARTER OK"
            exit 0
        else
            echo "SMARTER CRITICAL"
            exit 2
        fi
     else
        echo "SMARTER UNKNOWN"
        exit 3
     fi

}


main() {
    if [[ -z "${ARGS}" ]]
    then
        usage
    else
        probe
    fi
}
main

