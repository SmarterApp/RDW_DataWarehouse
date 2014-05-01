#!/bin/env bash

node_id=$1
host_name=$2
port=$3
pcp_user=postgres
pcp_pass=postgres

COMMAND_TEST="nc -w 1 $host_name $port"
COMMAND_ATTACH="/usr/bin/pcp_attach_node 100 localhost 9898 postgres postgres $node_id"

wait_for_host_to_recover() {
    eval $COMMAND_TEST
    while [ $? -ne 0 ]; do
       eval $COMMAND_TEST
    done
    eval $COMMAND_ATTACH
}

wait_for_host_to_recover &
