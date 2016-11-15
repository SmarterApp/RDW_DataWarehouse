#!/bin/bash

message_box(){
    t="$@xxxx"
    c=${replace:--}
    echo ${t//?/$c}
    echo "$c $@ $c"
    echo ${t//?/$c}
}

verbose_message(){
    if ( $VERBOSE ); then
        echo "$@"
    fi
}

rm_dir_if_exist(){
    if [ -d "$1" ]; then
        echo "Remove: $1"
        rm -r "$1"
        echo "Remove directory: $1"
        rm -rf "$1"
    fi
}

rm_file_if_exist(){
    if [ -f "$1" ]; then
        echo "Remove: $1"
        rm -r "$1"
        echo "Remove file: $1"
        rm -rf "$1"
    fi
}

validate_operation_status(){
    if [ $? != 0 ]; then
        message_box "Operation failed: $@" >&2
        exit 1
    fi
}
