'''
Created on May 3, 2013

@author: dip
'''
from celery import Celery
import os
from pdfmaker import celeryconfig

celery = Celery('pdf')
# configuration
config = celeryconfig.CeleryConfig()
celery.config_from_object(config)

def start():
    '''
    Start celery.  Intended for dev mode
    '''
    here = os.path.abspath(os.path.dirname(__file__))
    current_dir = os.getcwd()
    try:
        os.chdir(here)
        args = ['celery', 'worker', '--app', 'pdfmaker.pdf']
        celery.start(args)
    finally:
        os.chdir(current_dir)


def stop():
    '''
    Stop Celery
    '''
    celery.close()


if __name__ == '__main__':
    start()
