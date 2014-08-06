'''
Created on Jul 28, 2014

@author: tosako
'''


import os
from smarter_score_batcher.celery import celery


@celery.task(name="tasks.extract.separator")
def remote_write(path, data, mode=0o700):
    # create directory
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(str.encode(data) if type(data) is str else data)
        written = True
    if os.path.exists(path):
        os.chmod(path, mode)
    return written if written else False
