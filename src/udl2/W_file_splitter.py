from __future__ import absolute_import
from udl2.celery import celery
import time
import random


@celery.task(name="W_file_splitter.task")
def task(msg):
    # randomize delay seconds
    time.sleep(random.random() * 100)
    return msg