from __future__ import absolute_import

from celery_conf import celery
from file_splitter import split_file
import time


@celery.task
def file_splitter_task(msg):
    # splitted_files = file_splitter_impl(msg)
    splitted_files = split_file(msg['input_file'], output_path=msg['output_path'])
    print('splitted files', splitted_files)
    for file_name in splitted_files:
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
def file_splitter_impl(msg):
    parts = int(msg['parts'])
    input_file = msg['input_file'][0:-4]
    print("Doing file splitting... Got parameters --", msg)
    time.sleep(3)
    print("%i sub files are generated..." % parts)
    file_list = [input_file + '_part_' + str(i + 1) + '.csv' for i in range(parts)]
    return file_list
