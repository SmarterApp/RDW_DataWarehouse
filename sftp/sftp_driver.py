"""
Created on Oct 17, 2013

Module to initialize sftp zones and creating groups
"""

__author__ = 'sravi'

import argparse
from src import initialize_sftp_zone

if __name__ == "__main__":
    """
    Driver script to build and maintain sftp machine
    """
    parser = argparse.ArgumentParser(description='Process sftp driver args')
    parser.add_argument('-sh', '--home', dest="sftp_home", help='home folder for sftp')

    args = parser.parse_args()
    print("SFTP home: " + args.sftp_home)

    initialize_sftp_zone.initialize(args.sftp_home)
