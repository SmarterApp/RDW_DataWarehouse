#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: ${0##*/} username password [virtual_host]"
    exit 192
fi

declare username=$1
declare password=$2
declare vhost="/"

if [ $# -eq 3 ]; then
    vhost=$3
else
    echo "Use default virtual host $vhost"
fi


#make sure server running
server_pid=$(ps -f | grep 'rabbitmq-server' | grep -v 'grep' | awk '{print $2}')
if [ -z "$server_pid" ]; then
    echo "RabbitMQ is not running.., please start it first" >&2
    exit 192
fi

# check if user exists
user_exist=$(rabbitmqctl list_users | grep -w "$username")

if [ -n "$user_exist" ];
then
    echo "User $username already exists!" >&2
    exit 192
fi

#add new user
rabbitmqctl add_user "$username" "$password"

#set permission for new user
rabbitmqctl set_permissions -p "$vhost" "$username" ".*" ".*" ".*"

echo "Successfully create RabbitMQ user $username"
exit 0
