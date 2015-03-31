from smarter_score_batcher.celery import celery
from datetime import datetime


@celery.task(name='tasks.health_check')
def health_check():
    '''
    Return heartbeat message with current timestamp. The task caller can check timestamp to see
    validation of message but it is not require to check.

    The heartbeat message should sent via health_check queue.
    '''
    heartbeat = "heartbeat:" + str(datetime.now())
    return heartbeat
