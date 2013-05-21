from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from sfv.simple_file_validator import SimpleFileValidator
import os
import udl2.W_file_splitter

logger = get_task_logger(__name__)

# Keys for the initial incoming message
LANDING_ZONE_FILE = 'landing_zone_file'
BATCH_ID = 'batch_id'

@celery.task(name="udl2.W_file_validator.task")
def task(msg):
    # TODO: Break apart landing zone file and path in incoming message
    landing_zone_file = msg[LANDING_ZONE_FILE]
    landing_zone_file_name = os.path.basename(landing_zone_file)
    landing_zone_file_path = os.path.dirname(landing_zone_file)
    batch_sid = msg[BATCH_ID]

    sfv = SimpleFileValidator()
    error_list = sfv.execute(landing_zone_file_path, landing_zone_file_name, batch_sid)
    # TODO: Add logic that checks error list and writes to a log/db/etc

    return msg