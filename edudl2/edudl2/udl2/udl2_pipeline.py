import datetime
from celery import chain
from edudl2.preetl.pre_etl import pre_etl_job
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.udl2 import (W_file_arrived, W_file_decrypter, W_file_expander, W_get_load_type, W_get_callback_params,
                         W_simple_file_validator, W_file_splitter, W_file_content_validator,
                         W_load_json_to_integration, W_load_to_integration_table, W_parallel_csv_load,
                         W_determine_end_chain)
from edcore.utils.utils import merge_dict
__author__ = 'swimberly'


def get_pipeline_chain(archive_file, load_type='Unknown', file_parts=4, batch_guid_forced=None, initial_msg=None):
    """
    Get the celery chain object that is the udl pipeline

    :param archive_file:
    :param load_type:
    :param file_parts:
    :param batch_guid_forced:
    :return: a celery chain that contains the pipeline tasks
    """
    # Prepare parameters for task msgs
    guid_batch = pre_etl_job(udl2_conf, load_type=load_type, batch_guid_forced=batch_guid_forced)
    if guid_batch is None:
        print("CANNOT GENERATE guid_batch in PRE ETL, UDL2 PIPELINE STOPPED")
        return

    lzw = udl2_conf['zones']['work']
    jc_batch_table = udl2_conf['udl2_db']['batch_table']

    # generate common message for each stage
    common_msg = _generate_common_message(jc_batch_table, guid_batch, load_type, file_parts, initial_msg)
    arrival_msg = _generate_message_for_file_arrived(archive_file, lzw, common_msg)

    pipeline_chain = chain(W_file_arrived.task.si(arrival_msg),
                           W_file_decrypter.task.s(), W_file_expander.task.s(),
                           W_get_load_type.task.s(), W_get_callback_params.task.s(),
                           W_simple_file_validator.task.s(), W_file_splitter.task.s(),
                           W_parallel_csv_load.task.s(),
                           W_file_content_validator.task.s(), W_load_json_to_integration.task.s(),
                           W_load_to_integration_table.task.s(),
                           # The end tasks are in the W_determine_end_chain.py file until we resolve the awkward 3 way dependency
                           W_determine_end_chain.task.s())

    return pipeline_chain


def _generate_common_message(jc_batch_table, guid_batch, load_type, file_parts, initial_msg):
    initial_msg = {} if initial_msg is None else initial_msg
    msg = {
        mk.BATCH_TABLE: jc_batch_table,
        mk.GUID_BATCH: guid_batch,
        mk.LOAD_TYPE: load_type,
        mk.PARTS: file_parts,
        mk.START_TIMESTAMP: datetime.datetime.now()
    }
    return merge_dict(initial_msg, msg)


def _generate_message_for_file_arrived(archive_file, lzw, common_message):
    msg = {
        mk.INPUT_FILE_PATH: archive_file,
        mk.LANDING_ZONE_WORK_DIR: lzw
    }
    return merge_dict(common_message, msg)
