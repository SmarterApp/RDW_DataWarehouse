#!/bin/env python
from __future__ import absolute_import
import os
import shutil
import glob
import argparse
from edudl2.udl2.udl2_pipeline import get_pipeline_chain
from edudl2.udl2.udl_trigger import udl_trigger
from edudl2.udl2.celery import celery, udl2_conf, udl2_flat_conf


def run_pipeline(archive_file=None, batch_guid_forced=None):
    """
    Begins the UDL Pipeline process for the file found at path archive_file

    :param archive_file: The file to be processed
    :param batch_guid_forced: this value will be used as batch_guid for the current run
    """
    if not archive_file:
        raise Exception
    get_pipeline_chain(archive_file, batch_guid_forced=batch_guid_forced).delay()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='archive_file', help="path to the source archive file.")
    parser.add_argument('--dev', action='store_true', dest='dev_mode',
                        default=False, help="dev mode (Celery will run as eager and file is optional)")
    parser.add_argument('-g', dest='batch_guid_forced', default=None,
                        help="force the udl2 pipeline to use this batch guid")
    parser.add_argument('--loop', dest='loop', action='store_true',
                        help='Runs the udl_trigger script to watch the arrivals directory and schedule pipeline')
    args = parser.parse_args()
    if args.dev_mode:
        # TODO: Add to ini for $PATH and eager mode when celery.py is refactored
        celery.conf.update(CELERY_ALWAYS_EAGER=True)
        os.environ['PATH'] += os.pathsep + '/usr/local/bin'
        if args.archive_file is None:
            src_dir = os.path.join(os.path.dirname(__file__), '..', 'edudl2', 'tests', 'data', 'test_data_latest')
            # Find the first tar.gz.gpg file as LZ file
            file_name = glob.glob(os.path.join(src_dir, "*.tar.gz.gpg"))[0]
            # Copy file to arrivals dir of ca tenant
            dest = os.path.join(udl2_conf['zones']['arrivals'], 'ca', os.path.basename(file_name))
            shutil.copy(file_name, dest)
            args.archive_file = dest

    if args.loop:
        # run the udl trigger to watch the arrivals directory and schedule pipeline
        udl_trigger(udl2_flat_conf)
    elif args.dev_mode or args.archive_file is not None:
        # run the pipeline for a single file
        run_pipeline(args.archive_file, batch_guid_forced=args.batch_guid_forced)
    else:
        parser.error('Please specify a valid argument')
