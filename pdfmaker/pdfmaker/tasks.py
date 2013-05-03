'''
Created on May 2, 2013

@author: tosako
'''
from celery import Celery
celery = Celery('pdfmaker', backend='amqp', broker='amqp://guest@localhost//', include=['tasks'])
# print("celery: " + celery)

@celery.task
def add(x, y):
    return x + y


@celery.task
def mul(x, y):
    return x * y


@celery.task
def xsum(numbers):
    return sum(numbers)
