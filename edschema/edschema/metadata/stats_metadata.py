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
Created on Jun 19, 2013

@author: tosako
'''
from sqlalchemy.schema import MetaData, Table, Column, Index
from sqlalchemy.types import String, DateTime, BigInteger, Text


def generate_stats_metadata(schema_name=None, bind=None):
    metadata = MetaData(schema=schema_name, bind=bind)
    udl_stats = Table('udl_stats', metadata,
                      Column('rec_id', BigInteger, primary_key=True),
                      Column('tenant', String(32), nullable=False),
                      Column('load_type', String(32), nullable=False),
                      Column('file_arrived', DateTime, nullable=False),
                      Column('load_start', DateTime, nullable=True),
                      Column('load_end', DateTime, nullable=True),
                      Column('load_status', String(32), nullable=False),
                      Column('batch_guid', String(50), nullable=False),
                      Column('record_loaded_count', BigInteger, nullable=True),
                      Column('last_pdf_task_requested', DateTime, nullable=True),
                      Column('last_pre_cached', DateTime, nullable=True),
                      Column('batch_operation', String(1), nullable=True),
                      Column('snapshot_criteria', String(), nullable=True),
                      Column('notification', String(), nullable=True),
                      Column('notification_status', String(), nullable=True)
                      )
    Index('udl_stats_load_status_type_idx', udl_stats.c.load_status, udl_stats.c.load_type, unique=False)

    extract_stats = Table('extract_stats', metadata,
                          Column('request_guid', String(50), nullable=False),
                          Column('timestamp', DateTime, nullable=True),
                          Column('status', String(32), nullable=False),
                          Column('task_id', String(50), nullable=True),
                          Column('celery_task_id', String(50), nullable=True),
                          Column('info', Text, nullable=True)
                          )
    return metadata
