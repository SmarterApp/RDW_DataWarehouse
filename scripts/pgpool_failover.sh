#!/bin/env bash

node_id=$1
host_name=$2
port=$3
pcp_user=postgres  # replace this with your pcp.conf user name if necessary
pcp_pass=postgres  # replace this with your pcp.conf password if necessary
pcp_host=localhost
pcp_port=9898     # replace this with your pcp.conf pgpool.conf pcp port if necessary
attach_timeout=100
pgpool_status_file=/var/log/pgpool-II/pgpool_status # replace with your pgpool_status file location

# command to check pgpool parent is running or not
COMMAND_PS="ps -C pgpool|wc -l"
# command to check failover host name
COMMAND_TEST="nc -w 1 $host_name $port"
# command to reattach node to pgpool. change port number and user name, password
COMMAND_ATTACH="/usr/bin/pcp_attach_node $attach_timeout localhost $pcp_port $pcp_user $pcp_pass $node_id"

wait_for_host_to_recover() {
    eval $COMMAND_TEST
    while [ $? -ne 0 ]; do
       PARENT=`eval $COMMAND_PS`
       if [ $PARENT -eq "1" ]; then

          rm $pgpool_status_file
          exit
       fi
       eval $COMMAND_TEST
    done
    eval $COMMAND_ATTACH
}

wait_for_host_to_recover &