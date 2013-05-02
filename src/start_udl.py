#!/usr/bin/env python
import subprocess


def start_rabbitmq(RABBITMQ_SERVER):
    subprocess.call(["/usr/bin/sudo", RABBITMQ_SERVER])

if __name__ == '__main__':
    RABBITMQ_SERVER='/opt/local/sbin/rabbitmq-server'
    start_rabbitmq(RABBITMQ_SERVER)

