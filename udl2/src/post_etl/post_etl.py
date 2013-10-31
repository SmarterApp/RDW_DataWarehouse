import os
import argparse
import logging

__author__ = 'sravi'

logger = logging.getLogger(__name__)


def cleanup_work_zone(batch_guid):
    return True

if __name__ == "__main__":
    """
    Entry point to post_etl to run as stand alone script
    """
    parser = argparse.ArgumentParser(description='Process post etl args')
    parser.add_argument('-g', '--batch_guid', dest='batch_guid',
                        help='Batch GUID of the process work zone which needs cleanup')

    args = parser.parse_args()
    if args.batch_guid:
        print('Cleanup work zone for process with GUID: ' + args.batch_guid)
        if cleanup_work_zone(args.batch_guid):
            print('Cleanup complete successfully')
        else:
            print('Cleanup failed')