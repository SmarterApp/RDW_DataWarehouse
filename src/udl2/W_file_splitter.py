from __future__ import absolute_import
from udl2.celery import celery
import time
import random


@celery.task
def task(msg):
    # randomize delay seconds
    time.sleep(random.random() * 10)
    return msg