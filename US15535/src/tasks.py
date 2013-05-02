from __future__ import absolute_import

from celery_conf import celery
import time


@celery.task
def file_splitter_mock_task(msg):
    mock_files = file_splitter_impl()
    for file_name in mock_files:
        file_loader_mock_task.apply_async([file_name], queue='Q_files_to_be_loaded')


@celery.task
def file_loader_mock_task(msg):
    time.sleep(2)
    print('doing file loading for...' + str(msg))


@celery.task
def add(x, y):
    return x + y


@celery.task
def mul(x, y):
    return x * y


@celery.task
def xsum(numbers):
    return sum(numbers)


# this function will be replaced by US15440
def file_splitter_impl():
    print("Doing file splitting...")
    time.sleep(3)
    print("Four sub files are generated...")
    return ['file1', 'file2', 'file3', 'file4']
