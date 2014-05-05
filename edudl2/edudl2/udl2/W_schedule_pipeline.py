__author__ = 'sravi'

import os
from edudl2.udl2.celery import celery
from celery.utils.log import get_task_logger
import edudl2.udl2.udl2_pipeline as udl2_pipeline

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_schedule_pipeline.schedule_pipeline")
def schedule_pipeline(archive_file):
    """Point of entry task to start the pipeline chain

    :param archive_file: path of the file which needs to be run through the pipeline
    """
    if not archive_file or not os.path.exists(archive_file):
        logger.error('W_schedule_pipeline: Scheduling pipeline failed due to invalid file <%s>' % archive_file)
        raise Exception('Scheduling pipeline failed due to invalid file')

    logger.info('W_schedule_pipeline: Scheduling pipeline for file <%s>' % archive_file)
    udl2_pipeline.get_pipeline_chain(archive_file).delay()
    return True
