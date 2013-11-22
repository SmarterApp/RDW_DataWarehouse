__author__ = 'swimberly'

import glob
import os

from celery.result import AsyncResult

from udl2.udl2_pipeline import get_pipeline_chain
from udl2.celery import celery
from udl2 import message_keys as mk
from udl2.celery import udl2_conf


@celery.task(name="udl2.W_get_udl_file.get_next_file")
def get_next_file(msg):
    """
    Look in the tenants arrival folder for new files, if there is a file present
    move to the next step of the pipeline, otherwise what for x amount of time and look again
    :param msg: A dictionary containing at least: mk.TENANT_SEARCH_PATHS, mk.PARTS, mk.LOAD_TYPE
    :return: A string stating if the task found a file
    """

    tenant_dirs = msg[mk.TENANT_SEARCH_PATHS]

    files_in_dir = []
    for tenant_dir in tenant_dirs:
        print("checking tenant directory:", tenant_dir)
        files_in_dir += glob.glob(os.path.join(tenant_dir, '*'))

    # may need to add additional checks for incomplete files
    # sort files by time created
    print('files in dir', files_in_dir)
    files_in_dir = sorted(files_in_dir, key=lambda x: os.stat(x).st_mtime)
    print('files in dir', files_in_dir)

    next_file_msg = {
        mk.TENANT_SEARCH_PATHS: tenant_dirs,
        mk.PARTS: msg[mk.PARTS],
        mk.LOAD_TYPE: msg[mk.LOAD_TYPE],
    }

    if len(files_in_dir) > 0:
        print('picking up file:', files_in_dir[0])
        pipeline = get_pipeline_chain(files_in_dir[0], msg[mk.LOAD_TYPE], msg[mk.PARTS])
        (pipeline | get_next_file.si(next_file_msg)).apply_async(link_error=error_handler.s())
        return "File found and pipeline scheduled"
    else:
        get_next_file.apply_async((next_file_msg,), countdown=udl2_conf['search_wait_time'])
        return "No file found"


@celery.task(name="udl2.W_get_udl_file.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=True)
    print('Task %r raised exception: %r\n%r' % (
          uuid, exc, result.traceback))