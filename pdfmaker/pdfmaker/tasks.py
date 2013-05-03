'''
Created on May 2, 2013

@author: tosako
'''


from celery import Celery

celery = Celery('tasks', broker='amqp://guest@localhost//')

@celery.task
def add(x, y):
    return x + y
