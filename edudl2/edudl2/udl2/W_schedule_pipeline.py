# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

__author__ = 'sravi'

import os
from edudl2.udl2.celery import celery
from celery.utils.log import get_task_logger
import edudl2.udl2.udl2_pipeline as udl2_pipeline
from edudl2.udl2.constants import Constants as Const

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_schedule_pipeline.schedule_pipeline")
def schedule_pipeline(archive_file):
    """Point of entry task to start the pipeline chain

    :param archive_file: path of the file which needs to be run through the pipeline
    """
    if not archive_file or not os.path.exists(archive_file):
        logger.error('W_schedule_pipeline: Scheduling pipeline failed due to invalid file <%s>' % archive_file)
        raise Exception('Scheduling pipeline failed due to invalid file')

    # rename the file to mark it as scheduled for processing before submitting task to pipeline.
    # this is needed to avoid the udl trigger from rescheduling the pipeline in case of delay
    archive_file_for_processing = archive_file + Const.PROCESSING_FILE_EXT
    os.rename(archive_file, archive_file_for_processing)
    logger.info('W_schedule_pipeline: Scheduling pipeline for file <%s>' % archive_file_for_processing)
    udl2_pipeline.get_pipeline_chain(archive_file_for_processing).delay()
