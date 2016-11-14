#!/bin/bash

__dependencies(){
    packages=(edschema smarter)
    setup_virtualenv
}

_import_data_for_tenant(){
    if [ -z "$1" -o -z "$2" -o -z "$3" ]; then
        message_box "_import_data_for_tenant: 3 params required"
        exit -1
    fi
    echo "Import data for tenant: '$1' '$2' '$3'"
    cd "$EDWARE_WORKSPACE/test_utils"

    # python_3_3 import_data.py -c $EDWARE_INI_HOME/$EDWARE_INI_SMARTER -t cat -s CA -n "California"
    python_3_3 import_data.py -c "$EDWARE_INI_HOME/$EDWARE_INI_SMARTER" -t "$1" -s "$2" -n "$3" #TODO: support several words for '-n' param
    validate_operation_status "Unable to import data for tenant: '$1' '$2' '$3'"
}

__db(){
    generate_schema "edware" "edware_sds_1_38" "edware"
    generate_schema "edware" "edware_sds_1_38_dog" "edware"
    generate_schema "edware" "edware_sds_1_38_fish" "edware"

    _import_data_for_tenant "cat" "NC" "North_Carolina"
    _import_data_for_tenant "dog" "CA" "California"
    _import_data_for_tenant "fish" "VT" "Vermont"
}

__ini(){
    cp "$EDWARE_INI_SOURCE/$EDWARE_INI_SMARTER" "$EDWARE_INI_HOME"
}

__run(){
    echo "Run Smarter..."
    cd "$EDWARE_INI_HOME"
    pserve "$EDWARE_INI_SMARTER" >> "$EDWARE_LOG_SMARTER" 2>&1 &
}

__stop(){
    process_stop "[p]serve $EDWARE_INI_SMARTER"
}

__verify(){
    process_verify "[p]serve $EDWARE_INI_SMARTER"
}