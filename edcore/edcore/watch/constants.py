# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

__author__ = 'sravi'


class WatcherConstants():
    """
    constants related to watcher module
    """
    FILE_STAT_WATCH_INTERVAL = 'file_stat_watch_interval'
    FILE_STAT_WATCH_PERIOD = 'file_stat_watch_period'
    FILE_SYSTEM_SCAN_DELAY = 'file_system_scan_delay'
    FILE_CHECKSUM_THRESHOLD_WAIT_PERIOD = 'file_checksum_threshold_wait_period'
    BASE_DIR = 'base_dir'
    SOURCE_DIR = 'source_dir'
    DEST_DIR = 'dest_dir'
    FILE_PATTERNS_TO_WATCH = 'file_patterns_to_watch'
    CHECKSUM_FILE_EXTENSION = '.done'
    STAGING_DIR = 'staging_dir'


class MoverConstants():
    """
    constants related to mover module
    """
    LANDING_ZONE_HOSTNAME = 'landing_zone_hostname'
    SFTP_USER = 'sftp_user'
    PRIVATE_KEY_FILE = 'private_key_file'
    ARRIVALS_PATH = 'arrivals_path'
    FILE_TENANT = 'file_tenant'
    FILE_USER = 'file_user'
    FILE_MOVE_TYPE = 'file_move_type'
