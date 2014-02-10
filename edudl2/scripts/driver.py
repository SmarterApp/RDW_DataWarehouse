#!/bin/env python
from __future__ import absolute_import
import os
import argparse
import time

from edudl2.udl2.udl2_pipeline import get_pipeline_chain
from edudl2.udl2.W_get_udl_file import get_next_file

from edudl2.udl2 import message_keys as mk
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE


def start_pipeline(archive_file=None, load_type='Unknown', file_parts=4, batch_guid_forced=None, tenant_dirs=None):
    '''
    Begins the UDL Pipeline process by copying the file found at 'archive_file' to the landing zone arrivals dir and
    initiating our main pipeline chain.

    :param archive_file: The archive file that gets uploaded to the "Landing Zone" Arrivals dir beginning the UDL process
    :type archive_file: str
    :param udl2_conf: udl2 system configuration dictionary
    :type udl2: dict
    '''

    if archive_file:
        get_pipeline_chain(archive_file, load_type, file_parts, batch_guid_forced).delay()
    elif tenant_dirs:
        msg = {
            mk.TENANT_SEARCH_PATHS: tenant_dirs,
            mk.PARTS: file_parts,
            mk.LOAD_TYPE: load_type,
        }

        get_next_file.apply_async((msg,))


def create_unique_file_name(file_path):
    '''
    Given the path to a file, this function takes the file name, x, and appends a timestamp, t, to it, creating the name
    x_t.  This is used to prevent overwriting existing files in the "Landing Zone."

    :param file_path: The file whose name will be used as a template to create a new file name.
    :type file_path: str
    '''

    # This will return the name of the file and the extension in a tuple
    file_name_and_ext = os.path.splitext(os.path.basename(file_path))
    # Get the current time in seconds since the epoch
    time_stamp = int(time.time())
    new_file_name = '%s_%d%s' % (file_name_and_ext[0], time_stamp, file_name_and_ext[1])
    return new_file_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='archive_file', help="path to the source archive file.")
    parser.add_argument('-g', dest='batch_guid_forced', default=None, help="force the udl2 pipeline to use this batch guid")
    parser.add_argument('-t', dest='apply_transformation_rules', default='True', help="apply transformation rules or not")
    parser.add_argument('-f', dest='config_file', default=UDL2_DEFAULT_CONFIG_PATH_FILE, help="configuration file for UDL2")
    parser.add_argument('-p', dest='file_parts', default=4, type=int, help="The number or parts that the given csv file should be split into. Default=4")
    parser.add_argument('--loop-dirs', nargs='+', help='a list of white space separated directories that specify '
                                                       'the tenant directories to be observed')
    args = parser.parse_args()

    start_pipeline(args.archive_file, file_parts=args.file_parts, batch_guid_forced=args.batch_guid_forced,
                   tenant_dirs=args.loop_dirs)
