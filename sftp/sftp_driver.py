"""
Created on Oct 17, 2013

Module to initialize sftp zones and creating groups
"""

__author__ = 'sravi'

import argparse
from src.configure_sftp_zone import initialize, cleanup
from src.sftp_config import sftp_conf

if __name__ == "__main__":
    """
    Driver script to build and maintain sftp machine
    This script needs to be run as root user
    """
    parser = argparse.ArgumentParser(description='Process sftp driver args')
    parser.add_argument('--init', dest='driver_init_action', action='store_true')
    parser.add_argument('--cleanup', dest='driver_init_action', action='store_false')
    parser.set_defaults(driver_init_action=True)
    args = parser.parse_args()
    if args.driver_init_action:
        initialize(sftp_conf)
    else:
        cleanup(sftp_conf)