'''
Created on May 3, 2013

@author: dip
'''
from celery import Celery
from pdfmaker import celeryconfig


celery = Celery('pdf')
celery.config_from_object(celeryconfig)

if __name__ == '__main__':
    celery.start()
