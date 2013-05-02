from __future__ import absolute_import
from udl2.celery import celery
import time
import random


@celery.task(name="udl2.W_file_loader.task")
def task(msg):
    # randomize delay second
    time.sleep(random.random() * 100)
    return msg