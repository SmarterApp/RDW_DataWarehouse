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

'''
Created on Mar 21, 2015

@author: tosako
'''
import os
from edcore.utils.aws import S3_buckup
import time
import logging
import shutil
import traceback


logger = logging.getLogger('edudl2')


def archive_files(src_dir, s3_bucket, s3_to_glacier_after_days, prefix=None, backup_of_backup=None):
    timestamp = time.strftime('%Y%m%d%H%M')
    if prefix is None:
        prefix = timestamp
    else:
        prefix = os.path.join(prefix, timestamp)
    backup_filenames = []
    try:
        # create file list for archive
        for dirpath, dirs, files in os.walk(src_dir):
            for filename in files:
                fname = os.path.abspath(os.path.join(dirpath, filename))
                backup_filenames.append(fname)
        saved = True
        if backup_filenames:
            s3_backup = S3_buckup(s3_bucket, s3_to_glacier_after_days)
            for backup_filename in backup_filenames:
                archive_name = os.path.join(prefix, backup_filename[len(src_dir) + 1:])
                saved = saved and s3_backup.archive(backup_filename, archive_name)
                if not saved:
                    logger.error('Failed to archive, but save to backup of backup to archive later: ' + backup_filename)
                    # failed to archive.  save to backup of backup
                    if backup_of_backup is not None:
                        dest_path = os.path.join(backup_of_backup, archive_name)
                        if not os.path.exists(dest_path):
                            os.makedirs(dest_path, mode=0o750, exist_ok=True)
                        shutil.copy2(backup_filename, dest_path)
    except:
        # backup has an issue.  save in backup of backup.
        saved = False
        if backup_filenames and backup_of_backup is not None:
            logger.error(traceback.format_exc())
            logger.error('File could not be archived in S3.  Saving to backup of backup: ' + backup_of_backup)
            for file in backup_filenames:
                dest_path = os.path.dirname(os.path.join(backup_of_backup, prefix, file[len(src_dir) + 1:]))
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path, mode=0o750, exist_ok=True)
                shutil.copy2(file, dest_path)
    return saved
