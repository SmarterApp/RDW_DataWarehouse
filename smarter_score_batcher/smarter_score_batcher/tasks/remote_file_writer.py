'''
Created on Jul 28, 2014

@author: tosako
'''


from smarter_score_batcher.celery import celery
from smarter_score_batcher.utils.file_utils import file_writer


@celery.task(name="tasks.tsb.remote_writer")
def remote_write(path, data, mode=0o700):
    return file_writer(path, data, mode=mode)


@celery.task(name='task.tsb.update_metadata')
def update_metadata(file_path):
    pass