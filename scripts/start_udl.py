#!/usr/bin/env python
import subprocess

def start_celery():
    # we start celery by showing debug messages, and send event notifications
    try:
        subprocess.call(["celery worker --app=udl2 -l debug"], shell=True)    
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start_celery()
