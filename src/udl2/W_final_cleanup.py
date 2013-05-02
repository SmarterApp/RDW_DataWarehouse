from __future__ import absolute_import
from udl2.celery import celery
import time
import random


@celery.task(name="udl2.W_final_cleanup.task")
def task(msg):
    # randomize delay seconds
    time.sleep(random.random() * 100)
    return msg