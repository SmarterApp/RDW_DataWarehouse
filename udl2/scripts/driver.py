#!/bin/env python
from __future__ import absolute_import
import os
import argparse
import time
import datetime
import imp

from celery import chain
from udl2 import (W_file_arrived, W_file_decrypter, W_file_expander, W_simple_file_validator, W_file_splitter, W_file_content_validator,
                  W_load_json_to_integration, W_load_to_integration_table, W_load_from_integration_to_star, W_parallel_csv_load, W_all_done)
from udl2 import message_keys as mk
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from preetl.pre_etl import pre_etl_job


def start_pipeline(archive_file, udl2_conf, load_type='Assessment', file_parts=4, batch_guid_forced=None, **kwargs):
    '''
    Begins the UDL Pipeline process by copying the file found at 'archive_file' to the landing zone arrivals dir and
    initiating our main pipeline chain.

    @param archive_file: The archive file that gets uploaded to the "Landing Zone" Arrivals dir beginning the UDL process
    @type archive_file: str
    @param udl2_conf: udl2 system configuration dictionary
    @type udl2: dict
    '''

    # Prepare parameters for task msgs
    guid_batch = pre_etl_job(udl2_conf, load_type=load_type, batch_guid_forced=batch_guid_forced)
    #guid_batch = pre_etl_job(udl2_conf, load_type=load_type)
    if guid_batch is None:
        print("CANNOT GENERATE guid_batch in PRE ETL, UDL2 PIPELINE STOPPED")
        return

    lzw = udl2_conf['zones']['work']
    jc_batch_table = udl2_conf['udl2_db']['batch_table']

    # generate common message for each stage
    common_msg = generate_common_message(jc_batch_table, guid_batch, load_type, file_parts)
    arrival_msg = generate_message_for_file_arrived(archive_file, lzw, common_msg)
    all_done_msg = generate_all_done_msg(common_msg)

    pipeline_chain_1 = chain(W_file_arrived.task.si(arrival_msg), 
                             W_file_decrypter.task.s(), W_file_expander.task.s(),
                             W_simple_file_validator.task.s(), W_file_splitter.task.s(),
                             W_parallel_csv_load.task.s(),
                             W_file_content_validator.task.s(), W_load_json_to_integration.task.s(),
                             W_load_to_integration_table.task.s(),
                             W_load_from_integration_to_star.explode_to_dims.s(),
                             W_load_from_integration_to_star.explode_to_fact.s(),
                             W_all_done.task.si(all_done_msg))

    if kwargs.get('callback'):
        back_msg = {key: val for key, val in kwargs.items() if key != 'callback'}
        back_msg['batch_guid'] = guid_batch
        callback_task = kwargs['callback']

        # append the callback to the chain and run the chain
        (pipeline_chain_1 | callback_task.si(back_msg)).delay()

    else:
        pipeline_chain_1.delay()


def generate_common_message(jc_batch_table, guid_batch, load_type, file_parts):
    return {
            mk.BATCH_TABLE: jc_batch_table,
            mk.GUID_BATCH: guid_batch,
            mk.LOAD_TYPE: load_type,
            mk.PARTS: file_parts
        }


def generate_message_for_file_arrived(archive_file, lzw, common_message):
    msg = {
        mk.INPUT_FILE_PATH: archive_file,
        mk.LANDING_ZONE_WORK_DIR: lzw
    }
    return combine_messages(common_message, msg)


def generate_all_done_msg(common_message):
    msg = {
        mk.START_TIMESTAMP: datetime.datetime.now()
    }
    return combine_messages(common_message, msg)


def combine_messages(msg1, msg2):
    '''
    Combine two dictionary into one dictionary.
    If msg1 and msg2 has the same key, returns the value in the msg2
    '''
    return dict(list(msg1.items()) + list(msg2.items()))


def create_unique_file_name(file_path):
    '''
    Given the path to a file, this function takes the file name, x, and appends a timestamp, t, to it, creating the name
    x_t.  This is used to prevent overwriting existing files in the "Landing Zone."

    @param file_path: The file whose name will be used as a template to create a new file name.
    @type file_path: str
    '''

    # This will return the name of the file and the extension in a tuple
    file_name_and_ext = os.path.splitext(os.path.basename(file_path))
    # Get the current time in seconds since the epoch
    time_stamp = int(time.time())
    new_file_name = '%s_%d%s' % (file_name_and_ext[0], time_stamp, file_name_and_ext[1])
    return new_file_name


if __name__ == '__main__':
    '''
    Main function that reads parameters and kicks off the UDL Process
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='archive_file', required=True, help="path to the source archive file.")
    parser.add_argument('-g', dest='batch_guid_forced', default=None, help="force the udl2 pipeline to use this batch guid")
    parser.add_argument('-t', dest='apply_transformation_rules', default='True', help="apply transformation rules or not")
    parser.add_argument('-f', dest='config_file', default=UDL2_DEFAULT_CONFIG_PATH_FILE, help="configuration file for UDL2")
    parser.add_argument('-p', dest='file_parts', default=4, type=int, help="The number or parts that the given csv file should be split into. Default=4")
    args = parser.parse_args()

    if args.config_file is None:
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    else:
        config_path_file = args.config_file
    udl2_conf = imp.load_source('udl2_conf', config_path_file)
    from udl2_conf import udl2_conf
    start_pipeline(args.archive_file, udl2_conf, file_parts=args.file_parts, batch_guid_forced=args.batch_guid_forced)
