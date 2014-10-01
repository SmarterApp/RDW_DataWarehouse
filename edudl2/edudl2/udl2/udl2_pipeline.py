import datetime
from celery import chain
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk, W_load_err_file
from edudl2.udl2 import (W_file_arrived, W_file_decrypter, W_file_expander, W_get_load_type, W_get_params,
                         W_simple_file_validator, W_file_splitter, W_determine_end_chain)
from edcore.utils.utils import merge_dict
from uuid import uuid4
__author__ = 'swimberly'


def get_pipeline_chain(archive_file, load_type='Unknown', file_parts=4, guid_batch=None, initial_msg=None):
    """
    Get the celery chain object that is the udl pipeline

    :param archive_file:
    :param load_type:
    :param file_parts:
    :param batch_guid_forced:
    :return: a celery chain that contains the pipeline tasks
    """
    # Prepare parameters for task msgs
    guid_batch = str(uuid4()) if guid_batch is None else guid_batch
    lzw = udl2_conf['zones']['work']

    # generate common message for each stage
    arrival_msg = _generate_common_message(guid_batch, load_type, file_parts, archive_file, lzw, initial_msg)

    pipeline_chain = chain(W_file_arrived.task.si(arrival_msg),
                           W_file_decrypter.task.s(),
                           W_file_expander.task.s(),
                           W_get_load_type.task.s(),
                           W_get_params.task.s(),
                           W_simple_file_validator.task.s(),
                           W_load_err_file.task.s(),
                           W_file_splitter.task.s(),
                           # The end tasks are in the W_determine_end_chain.py file until we resolve the awkward 3 way dependency
                           W_determine_end_chain.task.s())

    return pipeline_chain


def _generate_common_message(guid_batch, load_type, file_parts, archive_file, lzw, initial_msg):
    initial_msg = {} if initial_msg is None else initial_msg
    msg = {
        mk.GUID_BATCH: guid_batch,
        mk.LOAD_TYPE: load_type,
        mk.PARTS: file_parts,
        mk.START_TIMESTAMP: datetime.datetime.now(),
        mk.INPUT_FILE_PATH: archive_file,
        mk.LANDING_ZONE_WORK_DIR: lzw
    }
    return merge_dict(initial_msg, msg)
