#!/bin/bash

generate_schema(){
    # 1 - database
    # 2 - schema
    # 3 - metadata
    # 4 - user
    # 5 - pass
    if [ -z "$1" -o -z "$2" -o -z "$3" ]; then
        message_box "generate_schema: 3 params required"
        exit -1
    fi
    if [ -z "$4" -o -z "$5" ]; then
        db_user="edware"
        db_pass="edware2013"
    else
        db_user="$4"
        db_pass="$5"
    fi

    echo "Create '$2' schema in '$1' database with '$3' metadata"
    if [ "$3" == "hpz" ]; then
        cd "$EDWARE_WORKSPACE/hpz/hpz/database"
    else
        cd "$EDWARE_WORKSPACE/edschema/edschema"
    fi

    python_3_3 metadata_generator.py -d $1 -s $2 -m $3 -a teardown  --host localhost:5432 -u $db_user -p $db_pass
    validate_operation_status "Unable to delete schema"

    python_3_3 metadata_generator.py -d $1 -s $2 -m $3 --host localhost:5432 -u $db_user -p $db_pass
    validate_operation_status "Unable to create schema"
}

setup_virtualenv(){
    for var in "${packages[@]}"; do
        message_box "Install $var package"
        local current=`pwd`
        cd "$EDWARE_WORKSPACE/$var"

        if [ -f setup-developer.py ];  then
           echo "Running setup-developer.py"
           python_3_3 setup-developer.py develop
        else
           echo "Running setup.py"
           python_3_3 setup.py develop
        fi

        validate_operation_status "Unable to set up Python's dependencies for '$var' package"
        cd "$current"
    done
}