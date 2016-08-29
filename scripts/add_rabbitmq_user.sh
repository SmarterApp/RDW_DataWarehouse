#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: ${0##*/} username password [virtual_host]"
    exit 192
fi

username=$1
password=$2
vhost="/"

if [ $# -eq 3 ]; then
    vhost=$3
else
    echo "Use default virtual host $vhost"
fi


#make sure server running
rabbitmqctl -q status > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "RabbitMQ is not running.., please start it first" >&2
    exit 192
fi

# check if user exists
user_exist=$(rabbitmqctl list_users | cut -f1 | grep -w "${username}")

if [ -n ${user_exist:-""} ]; then
    echo "User ${username} already exists!" >&2
    exit 192
fi

#add new user
rabbitmqctl add_user "${username}" "${password}"

#set permission for new user
rabbitmqctl set_permissions -p "${vhost}" "${username}" ".*" ".*" ".*"

ret=$?

if [ ${ret} -eq 0 ]; then
    echo "Successfully create RabbitMQ user ${username}"
else
    echo "Fail to set user ${username} permissions"
fi

exit ${ret}
