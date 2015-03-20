'''
Created on Mar 20, 2015

@author: tosako
'''
import boto
from boto.s3.lifecycle import Transition, Rule, Lifecycle
import os
import logging
from boto.exception import S3CreateError


logger = logging.getLogger('edcore')

def s3_backup(s3_bucket, prefix_dir, backup_filenames):
    # create s3 connection
    # create bucket if does not exist
    # create S3 connection if archive_S3_bucket name is specified
    if backup_filenames and s3_bucket is not None and s3_bucket:
        s3_conn = boto.connect_s3()
        # check if S3 bucket is created, if not create one.
        bucket = s3_conn.lookup(s3_bucket)
        if not bucket:
            # create bucket and lifecycle rule
            try:
                bucket = s3_conn.create_bucket(s3_bucket)
                to_glacier = Transition(days=30, storage_class='GLACIER')
                rule = Rule(id='file-grabber-rule1', status='Enabled', transition=to_glacier)
                lifecycle = Lifecycle()
                lifecycle.append(rule)
                bucket.configure_lifecycle(lifecycle)
            except S3CreateError:
                logger.error('failed to create S3 bucket[' + s3_bucket + ']. please check your AWS policy.')
                raise
            except:
                raise
        # upload file
        for backup_filename in backup_filenames:
            if os.path.exists(backup_filename):
                key = bucket.new_key(backup_filename[len(prefix_dir):])
                with open(backup_filename) as f:
                    key.set_contents_from_file(f)
                key.close()
        else:
            return False
        return True
