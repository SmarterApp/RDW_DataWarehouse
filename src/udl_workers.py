from celery import Celery
import time
import random

celery = Celery('udl_workers', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@celery.task
def W_file_splitter(msg):
    # randomize delay seconds
    time.sleep(random.random() * 10)
    return msg

@celery.task
def W_file_loader(msg):
    # randomize delay second
    time.sleep(random.random() * 10)
    return msg

@celery.task
def W_final_cleanup(msg):
    # randomize delay seconds
    time.sleep(random.random() * 10)
    return msg





