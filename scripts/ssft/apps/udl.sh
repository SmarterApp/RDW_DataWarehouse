#!/bin/bash

__dependencies(){
    echo "Set UDL dependencies"
    packages=(edudl2)
    setup_virtualenv
}

__db(){
    echo "Set UDL db"
    cd "$EDWARE_WORKSPACE/edudl2/scripts"
    generate_schema "edware_stats" "edware_stats" "stats"
}

__ini(){
    echo "Copy UDL ini"
    mkdir -p /opt/edware/conf
    cp "$EDWARE_INI_SOURCE/$EDWARE_INI_UDL" /opt/edware/conf
}

__run(){
    echo "Starting UDL"
    cd "$EDWARE_WORKSPACE/edudl2/scripts"
    sh start_celery.sh >> "$EDWARE_LOG_UDL 2>&1" &
}

__stop(){
    process_stop [c]elery
}

__verify(){
    process_verify [c]elery
}

_process_file(){
    cd "$EDWARE_WORKSPACE/edudl2/scripts"
    for file in `ls -1 $EDWARE_UDL_FILES_DEST`; do
        echo "Start processing of '$EDWARE_UDL_FILES_DEST/$file'"
        python3.3 driver.py --dev -a "$EDWARE_UDL_FILES_DEST/$file" >> "$EDWARE_LOG_UDL" 2>&1
        validate_operation_status "There are some errors during processing of '$EDWARE_UDL_FILES_DEST/$file'"
        echo "Complete processing of '$EDWARE_UDL_FILES_DEST/$file' successfully"
    done
}

__process_files(){
    DEFAULT_DATA="$EDWARE_WORKSPACE/edudl2/edudl2/tests/data/test_data_latest"
    if ! ([ -n "$EDWARE_UDL_MODE" ] && [ -n "$EDWARE_UDL_ARCHIVE_PREFIX" ] && [ -n "$EDWARE_UDL_FILES" ]); then
        echo "Usage:
        encryption-mode archive-name-prefix json-file csv-file      staging stg-cat test_data_latest/1.json test_data_latest/1.csv
        encryption-mode archive-name-prefix path                    local local-cat test_data_latest/*

        Files examples located in: $DEFAULT_DATA
        Mode:
            staging       encryption for staging environment
            local       encryption for local environment
        "
        exit -1
    fi

    if ! ([ "$EDWARE_UDL_MODE" = "staging" ] || [ "$EDWARE_UDL_MODE" = "local" ]); then
        message_box "Mode can be only 'staging' or 'local'"
        exit -1
    fi
    gz_arhive=$EDWARE_UDL_ARCHIVE_PREFIX.tar.gz
    tar -cvzf $gz_arhive --disable-copy $EDWARE_UDL_FILES
    validate_operation_status "Unable to zip files into $gz_arhive"

    message_box "Paraphrase:  sbac udl2"
    if [ "$EDWARE_UDL_MODE" = "staging" ]; then
        KEYS="$HOME/.gnupg/staging"
        echo "Staging encryption. Keys are in '$KEYS'."
        gpg --homedir $KEYS --armor --local-user ca_user@ca.com --recipient stg_sbac@smarterbalanced.org -e -s $gz_arhive
    else
        KEYS="$HOME/.gnupg/local"
        echo "Local encryption. Keys are in '$KEYS'."
        gpg --homedir $KEYS --armor --local-user ca_user@ca.com --recipient sbac_data_provider@sbac.com -e -s $gz_arhive
    fi

    validate_operation_status "Unable to prepare gpg archive"
    rm $gz_arhive
    mv $gz_arhive.asc $gz_arhive.gpg

    if [ "$EDWARE_UDL_MODE" = "staging" ]; then
        echo "Staging's archive is located in ${pwd}/$gz_arhive.gpg"
    else
        mv $gz_arhive.gpg "$EDWARE_UDL_FILES_DEST"
        echo "Generated files in $EDWARE_UDL_FILES_DEST"
        ls -1 "$EDWARE_UDL_FILES_DEST"
        message_box "Start processing of UDL archives"
        _process_file
        ls -1 "$EDWARE_UDL_FILES_DEST"
    fi
}
