from edudl2.file_finder.file_finder import find_files_in_directories
__author__ = 'swimberly'

from edudl2.udl2.celery import udl2_conf, celery
from edudl2.udl2 import message_keys as mk
import edudl2.udl2.udl2_pipeline as udl2_pipeline


@celery.task(name="udl2.W_get_udl_file.get_next_file")
def get_next_file(msg):
    """
    Look in the tenants arrival folder for new files, if there is a file present
    move to the next step of the pipeline, otherwise what for x amount of time and look again
    :param msg: A dictionary containing at least: mk.TENANT_SEARCH_PATHS, mk.PARTS, mk.LOAD_TYPE
    :return: A string stating if the task found a file
    """

    tenant_dirs = msg[mk.TENANT_SEARCH_PATHS]

    files_in_dir = find_files_in_directories(tenant_dirs)

    next_file_msg = {
        mk.LOOP_PIPELINE: True,
        mk.TENANT_SEARCH_PATHS: tenant_dirs,
        mk.PARTS: msg[mk.PARTS],
        # TODO: Load type is needed?
        mk.LOAD_TYPE: msg[mk.LOAD_TYPE],
    }

    if len(files_in_dir) > 0:
        print('picking up file:', files_in_dir[0])
        pipeline = udl2_pipeline.get_pipeline_chain(files_in_dir[0], msg[mk.LOAD_TYPE], msg[mk.PARTS], None, next_file_msg)
        (pipeline | get_next_file.si(next_file_msg)).apply_async()
        return "File found and pipeline scheduled"
    else:
        get_next_file.apply_async((next_file_msg,), countdown=udl2_conf['search_wait_time'])
        return "No file found"
