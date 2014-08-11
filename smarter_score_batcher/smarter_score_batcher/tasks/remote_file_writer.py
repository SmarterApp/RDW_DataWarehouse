'''
Created on Jul 28, 2014

@author: tosako
'''


from smarter_score_batcher.celery import celery
from smarter_score_batcher.utils.file_utils import file_writer


@celery.task(name="tasks.extract.separator")
def remote_write(path, data, mode=0o700):
    return file_writer(path, data, mode=mode)
