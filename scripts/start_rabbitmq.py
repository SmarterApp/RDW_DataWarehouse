#!/usr/bin/env python
import subprocess

def start_rabbitmq(RABBITMQ_SERVER):
    try:    
        subprocess.call(["sudo " +  RABBITMQ_SERVER + " &"], shell=True)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    RABBITMQ_SERVER='/opt/local/sbin/rabbitmq-server'
    start_rabbitmq(RABBITMQ_SERVER)
