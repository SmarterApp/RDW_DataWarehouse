#!/usr/bin/env python
import subprocess
import time

def start_rabbitmq(RABBITMQ_SERVER):
    try:    
        subprocess.call(["sudo " +  RABBITMQ_SERVER + " &"], shell=True)
    except Exception as e:
        print(e)

def start_celery():
    try:
        subprocess.call(["celery -A udl_workers worker"], shell=True)    
    except Exception as e:
        print(e)


if __name__ == '__main__':
    RABBITMQ_SERVER='/opt/local/sbin/rabbitmq-server'
    start_rabbitmq(RABBITMQ_SERVER)
    # wait for rabbit started
    time.sleep(10)
    start_celery()

