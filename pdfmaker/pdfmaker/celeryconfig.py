'''
Created on May 3, 2013

@author: dip
'''
# Broker setting
BROKER_URL = 'amqp://guest@localhost//'

# List of modules to import when celery starts
CELERY_INCLUDE = ("tasks",)

# Using rabbitmq for task state and results
CELERY_RESULT_BACKEND = 'amqp'

CELERYD_CONCURRENCY = '8'
