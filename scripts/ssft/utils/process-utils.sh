#!/bin/bash

_check_pattern(){
    if [ -z "$1" ]; then
        message_box "$2"
        exit -1
    fi
}

process_verify(){
    _check_pattern "$1" "Please specify pattern to find a process (e.g. [p]serve)."
    (
    verbose_message "Find process of '$1' $2"
    ps aux | grep "$1"
    ) || return 0 # exit always 0
}

process_stop (){
    _check_pattern "$1" "Please specify pattern to find a process and kill (e.g. [p]serve)."
    (
    verbose_message "Kill process of '$1'"
    PID=$(ps aux | grep "$1" | awk '{print $2}')
    if [ -n "$PID" ]; then
        verbose_message "PID: '$PID'"
        kill $PID
        sleep 5
        process_verify "$1" "after kill command"
    else
        echo "'$1' app isn't running"
    fi
    ) || return 0 # exit always 0
}