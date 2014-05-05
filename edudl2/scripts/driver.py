#!/bin/env python
from __future__ import absolute_import
import os
import argparse
from edudl2.udl2.udl2_pipeline import get_pipeline_chain
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2.celery import celery, udl2_flat_conf as udl2_conf
from edudl2.udl2.udl_trigger import udl_trigger
import shutil
import glob
import tempfile


def run_pipeline(archive_file=None, load_type='Unknown', file_parts=4, batch_guid_forced=None):
    '''
    Begins the UDL Pipeline process by copying the file found at 'archive_file' to the landing zone arrivals dir and
    initiating our main pipeline chain.

    :param archive_file: The archive file that gets uploaded to the "Landing Zone" Arrivals dir beginning the UDL process
    :type archive_file: str
    :param udl2_conf: udl2 system configuration dictionary
    :type udl2: dict
    '''
    if not archive_file:
        raise Exception
    get_pipeline_chain(archive_file, load_type, file_parts, batch_guid_forced).delay()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='archive_file', help="path to the source archive file.")
    parser.add_argument('--dev', action='store_true', dest='dev_mode', default=False, help="dev mode")
    parser.add_argument('-g', dest='batch_guid_forced', default=None, help="force the udl2 pipeline to use this batch guid")
    parser.add_argument('-f', dest='config_file', default=UDL2_DEFAULT_CONFIG_PATH_FILE, help="configuration file for UDL2")
    parser.add_argument('-p', dest='file_parts', default=4, type=int, help="The number or parts that the given "
                                                                           "csv file should be split into. Default=4")
    parser.add_argument('--loop', dest='loop', action='store_true',
                        help='Runs the udl_trigger script to watch the arrivals directory and schedule pipeline')
    args = parser.parse_args()
    if args.dev_mode:
        celery.conf.update(CELERY_ALWAYS_EAGER=True)
        os.environ['PATH'] += os.pathsep + '/usr/local/bin'
    if args.dev_mode and args.archive_file is None:
        # TODO: Add to ini for $PATH and eager mode when celery.py is refactored
        src_dir = os.path.join(os.path.dirname(__file__), '..', 'edudl2', 'tests', 'data', 'test_data_latest')
        # Find the first tar.gz.gpg file as LZ file
        file_name = glob.glob(os.path.join(src_dir, "*.tar.gz.gpg"))[0]
        dest = os.path.join(tempfile.mkdtemp(), os.path.basename(file_name))
        shutil.copy(file_name, dest)
        args.archive_file = dest
    if args.loop:
        # run the udl trigger to watch the arrivals directory and schedule pipeline
        udl_trigger(udl2_conf)
    else:
        run_pipeline(args.archive_file, file_parts=args.file_parts, batch_guid_forced=args.batch_guid_forced)
