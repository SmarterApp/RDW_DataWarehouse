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
    if prefix is None:
        prefix = time.strftime('%Y%m%d%H%M')
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
                        dest_path = os.path.join(backup_of_backup, backup_filename[len(src_dir) + 1])
                        if not os.path.exists(dest_path):
                            os.makedirs(dest_path, mode=0o750, exist_ok=True)
                        shutil.copy2(backup_filename, dest_path)
        if saved and backup_of_backup is not None:
            # s3 bucket is in operation
            # If there are unarchived file in backup of backup, then save
            return archive_files(backup_of_backup, s3_bucket, s3_to_glacier_after_days, prefix=prefix)
        return True
    except:
        # backup has an issue.  save in backup of backup.
        if backup_filenames and backup_of_backup is not None:
            logger.error(traceback.format_exc())
            logger.error('File could not be archived in S3.  Saving to backup of backup: ' + backup_of_backup)
            for file in backup_filenames:
                dest_path = os.path.dirname(os.path.join(backup_of_backup, prefix, file[len(src_dir) + 1:]))
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path, mode=0o750, exist_ok=True)
                shutil.copy2(file, dest_path)
    return False
