'''
Created on Jul 28, 2014

@author: tosako
'''


from edworker.celery import celery
import os


@celery.task(name="tasks.extract.separator")
def remote_write(path, data, mode=0o700):
    #create directory
    os.makedirs(os.path.dirname(path), mode, exist_ok=True)
    with open(path, 'w') as f:
        f.write(data)
    if os.path.exists(path):
        os.chmod(path, mode)
