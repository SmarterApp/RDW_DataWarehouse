#!/bin/bash

__dependencies(){
    packages=(edschema hpz smarter)
    setup_virtualenv
}

__db(){
    cd "$EDWARE_WORKSPACE/hpz/hpz/database"
    generate_schema "hpz" "hpz" "hpz" "hpz" "hpz2015"
}

__ini(){
    cp "$EDWARE_INI_SOURCE/$EDWARE_HPZ_INI" "$EDWARE_INI_HOME"
}

__run(){
    echo "Run HPZ..."
    cd "$EDWARE_INI_HOME"
    pserve $EDWARE_HPZ_INI >> $EDWARE_LOG_HPZ 2>&1 &
}

__stop(){
    process_stop "[p]serve $EDWARE_HPZ_INI"
}

__verify(){
    process_verify "[p]serve $EDWARE_HPZ_INI"
}
