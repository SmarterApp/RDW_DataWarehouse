from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from final_cleanup.final_cleanup import create_directory_structure_for_file_history

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_final_cleanup.task")
def task(msg):
    '''
    Celery task that handles clean-up of files created during the UDL process.
    It first creates a sub-directory within the history directory (using the name of the original file)
    It then moves the originally uploaded file (in the landing zone) to our history directory.
    It will also eventually move the split files (in the work zone) to the same history directory.
    This will have to wait until we implement Celery Chords, as we don't want to move work files
    until all the file-loaders have completed.

    @param msg: the message received from the penultimate step in the UDL process. Contains all params needed.
    @type msg: dict
    '''
    logger.info(task.name)
    landing_zone_file = msg['landing_zone_file']
    history = msg['history']
    history_directory = create_directory_structure_for_file_history(history, landing_zone_file)
    with open("test.log", 'a+') as f:
        #f.write(str(datetime.datetime.now()) + ': done with' + msg['csv_file_path'] + ' after ' + task.name + "\n")
        pass
    return msg


@celery.task(name="udl2.W_final_cleanup.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))