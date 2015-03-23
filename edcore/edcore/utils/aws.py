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

class S3_buckup:
    def __init__(self, bucket_name, s3_to_glacier_after_days=None):
        # create s3 connection
        # create bucket if does not exist
        # create S3 connection if archive_S3_bucket name is specified
        self.__bucket_name = bucket_name
        self.__s3_conn = boto.connect_s3()
        self.__bucket = self.__s3_conn.lookup(self.__bucket_name)
        if not self.__bucket:
            try:
                self.__bucket = self.__s3_conn.create_bucket(self.__bucket_name)
                if s3_to_glacier_after_days is not None:
                    to_glacier = Transition(days=s3_to_glacier_after_days, storage_class='GLACIER')
                    rule = Rule(id='archive-rule1', status='Enabled', transition=to_glacier)
                    lifecycle = Lifecycle()
                    lifecycle.append(rule)
                    self.__bucket.configure_lifecycle(lifecycle)
            except S3CreateError:
                logger.error('failed to create S3 bucket[' + self.__bucket_name + ']. please check your AWS policy.')
                raise

    def archive(self, src_file, archive_name):
        # upload file
        if os.path.exists(src_file):
            key = self.__bucket.new_key(archive_name)
            with open(src_file) as f:
                key.set_contents_from_file(f)
            key.close()
        else:
            return False
        return True
