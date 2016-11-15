#!/bin/bash

MEMCACHED="[m]emcached -d"
RABBIT="[r]abbitmq-server"

_smart_run(){
    FILTER="$1"
    COMMAND="$2"
    PID=$(ps aux | grep "$FILTER" | awk '{print $2}')
    if [ -z "$PID" ]; then
        eval "$COMMAND"
        validate_operation_status "Errors in run of '$COMMAND'"
        sleep 15 # wait for service is up
    fi
}

__run (){
    memcached_path=`which memcached`
    if [ -z "$memcached_path" ]; then
        memcached_path="/usr/local/bin/memcached"
    fi
    _smart_run "$MEMCACHED" "$memcached_path -d"

    rabbit_path=`which rabbitmq-server`
    if [ -z "$rabbit_path" ]; then 
        rabbit_path="/usr/local/sbin/rabbitmq-server"
    fi
    _smart_run "$RABBIT" "$rabbit_path >> /dev/null 2>&1 &"
}

__stop (){
    process_stop "$MEMCACHED"
    process_stop "$RABBIT"
}