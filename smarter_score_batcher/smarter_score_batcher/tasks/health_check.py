from smarter_score_batcher.celery import celery
from datetime import datetime
from sqlalchemy.sql.expression import select
from smarter_score_batcher.database.tsb_connector import TSBDBConnection
import logging


logger = logging.getLogger('smarter_score_batcher')


@celery.task(name='tasks.tsb.health_check')
def health_check():
    '''
    Return heartbeat message with current timestamp if DB connection passes.
    The task caller can check timestamp to see validation of message but it is not require to check.

    The heartbeat message should sent via health_check queue.
    '''
    try:
        with TSBDBConnection() as connector:
            query = select([1])
            results = connector.get_result(query)
            if not results:
                return "Cannot connect to TSB DB"
    except Exception as e:
        logger.error("Heartbeat cannot connect to TSB DB: %s", str(e))
        return "Cannot connect to TSB DB"
    heartbeat = "heartbeat:" + str(datetime.now())
    return heartbeat
