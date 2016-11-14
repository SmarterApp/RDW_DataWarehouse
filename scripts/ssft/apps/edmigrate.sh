#!/bin/bash

__dependencies(){
    packages=(edschema smarter edmigrate)
    setup_virtualenv
}

__db(){
    generate_schema "edware" "edware_sds_1_38_public" "edware"
}

__ini(){
    echo "Use Smarter ini"
}

__run_public_reports(){
    cd "$EDWARE_WORKSPACE/edmigrate/public_report"
    python3.3 copy_data.py -t cat -i "$EDWARE_INI_HOME/$EDWARE_INI_SMARTER" >> "$EDWARE_LOG_EDMIGRATE" 2>&1
    validate_operation_status "There are some errors in public reports migration. 'less \"$EDWARE_LOG_EDMIGRATE\"' for more details."
    message_box "Public reports data were processed successfully"
}

__run_udl_migration(){
    cd "$EDWARE_WORKSPACE/edmigrate/edmigrate"
    python3.3 main.py --migrateOnly -i "$EDWARE_INI_HOME/$EDWARE_INI_SMARTER" -t cat >> "$EDWARE_LOG_EDMIGRATE" 2>&1
    validate_operation_status "There are some errors in UDL data migration. 'less \"$EDWARE_LOG_EDMIGRATE\"' for more details."
    message_box "UDL data were processed successfully"
}
