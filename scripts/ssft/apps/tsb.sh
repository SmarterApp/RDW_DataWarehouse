#!/bin/bash

__dependencies(){
    mkdir -p /opt/edware/tsb/item_level
    mkdir -p /opt/edware/tsb/staging
    mkdir -p /opt/edware/tsb/assessments
    mkdir -p /opt/edware/tsb/raw_data
    packages=(smarter_score_batcher)
    setup_virtualenv
}

__db(){
    echo "There are no steps for installation of DB"
 }

__ini(){
    cp "$EDWARE_INI_SOURCE/$EDWARE_TSB_INI" "$EDWARE_INI_HOME"
}

__run(){
    echo "Run TSB..."
    cd "$EDWARE_INI_HOME"
    pserve $EDWARE_TSB_INI >> "$EDWARE_LOG_TSB" 2>&1 &
}

__stop(){
    process_stop "[p]serve $EDWARE_TSB_INI"
}

__verify(){
    process_verify "[p]serve $EDWARE_TSB_INI"
}
