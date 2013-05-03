'''
Created on May 3, 2013

@author: dip
'''
from celery import Celery
celery = Celery('pdfmaker', backend='amqp', broker='amqp://guest@localhost//', include=['tasks'])

if __name__ == '__main__':
    celery.start()