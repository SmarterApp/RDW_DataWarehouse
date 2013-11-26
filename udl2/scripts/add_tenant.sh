#!/bin/bash

set -e # Exit on errors

function create_tenant_schema {
    # initialize edware star schema for the tenant
    python -m edschema.metadata_generator --metadata edware -s edware_$1 -d edware --host=localhost:5432 -u edware -p edware2013
}

function drop_tenant_schema {
    # drop edware star schema for the tenant
    python -m edschema.metadata_generator --metadata edware -a teardown -s edware_$1 -d edware --host=localhost:5432 -u edware -p edware2013
}

function populate_tenant_master_meta_info {
    # populate the udl2.master_metadata table for the new tenant being added
    # TODO
    echo "TODO: populate_tenant_master_meta_info"
}

function clear_tenant_master_meta_info {
    # populate the udl2.master_metadata table for the new tenant being added
    # TODO
    echo "TODO: clear_tenant_master_meta_info"
}

function create_tenant_directories {
    # landing directories
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/landing/arrivals/$1
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/landing/work/$1
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/landing/history/$1

    #pickup directories
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/work/$1
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/departures/$1
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/history/$1

    # landing-work subdirectores
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/landing/work/$1/arrived
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/landing/work/$1/expanded
    sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/landing/work/$1/subfiles

}

function update_permissions {
     # landing directories
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/landing/arrivals/$1
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/landing/work/$1
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/landing/history/$1

    #pickup directories
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/work/$1
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/departures/$1
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/history/$1

    # landing-work subdirectores
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/landing/work/$1/arrived
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/landing/work/$1/expanded
    sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/landing/work/$1/subfiles
}

function remove_tenant_directories {
    # landing directories
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/landing/arrivals/$1
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/landing/work/$1
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/landing/history/$1

    #pickup directories
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/pickup/work/$1
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/pickup/departures/$1
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/pickup/history/$1

    # landing-work subdirectores
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/pickup/landing/work/$1/arrived
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/pickup/landing/work/$1/expanded
    sudo -u root -s rm -rf /opt/wgen/edware-udl/zones/pickup/landing/work/$1/subfiles
}

function get_opts {
    if ( ! getopts ":t:hcr" opt); then
        echo "Usage: `basename $0` options (-t tenant_name) (-c) (-r) -h for help"
        exit $E_OPTERROR;
    fi

    MODE='CREATE'
    while getopts "t:hcr" opt; do
        case $opt in
            t)
                # we may want to validate this value
                TENANT=$OPTARG 
                echo "Tenent:" $TENANT
                ;;
            c)
                echo "create mode"
                MODE="CREATE"
                ;;
            r)
                echo "remove mode"
                MODE="REMOVE"
                ;;
            h)
                show_help
                ;;
            ?)
                echo "invalid args"
                echo "Usage: `basename $0` options (-t tenant_name) -h for help"
                ;;
        esac
    done

}

function show_help {
    echo "#To add a tenant's relevant directories"
    echo "add_tenant.sh -t tenant_name"
}

function main {
    get_opts $@
    if [ ${MODE:=""} == "CREATE" ]; then
        create_tenant_directories $TENANT
        update_permissions $TENANT
        create_tenant_schema $TENANT
        populate_tenant_master_meta_info $TENANT
    elif [ ${MODE:=""} == "REMOVE" ]; then
        remove_tenant_directories $TENANT
        drop_tenant_schema $TENANT
        clear_tenant_master_meta_info $TENANT
    fi
}

main $@
