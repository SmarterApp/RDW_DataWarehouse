'''
Created on Jun 19, 2013

@author: tosako
'''
from sqlalchemy.schema import MetaData, Table, Column, Index
from sqlalchemy.types import String, DateTime, BigInteger, Text


def generate_stats_metadata(schema_name=None, bind=None):
    metadata = MetaData(schema=schema_name, bind=bind)
    udl_stats = Table('udl_stats', metadata,
                      Column('state_code', String(2), nullable=False),
                      Column('tenant', String(32), nullable=False),
                      Column('load_type', String(32), nullable=False),
                      Column('file_arrived', DateTime, nullable=False),
                      Column('load_start', DateTime, nullable=True),
                      Column('load_end', DateTime, nullable=True),
                      Column('load_status', String(32), nullable=False),
                      Column('batch_guid', String(50), nullable=False),
                      Column('record_loaded_count', BigInteger, nullable=True),
                      Column('last_pdf_task_requested', DateTime, nullable=True),
                      Column('last_pre_cached', DateTime, nullable=True)
                      )
    Index('udl_stats_load_status_type_idx', udl_stats.c.load_status, udl_stats.c.load_status, unique=False)

    extract_stats = Table('extract_stats', metadata,
                          Column('request_guid', String(50), nullable=False),
                          Column('timestamp', DateTime, nullable=True),
                          Column('status', String(32), nullable=False),
                          Column('task_id', String(50), nullable=True),
                          Column('celery_task_id', String(50), nullable=True),
                          Column('info', Text, nullable=True)
                          )

    Index('extract_stats_request_task_id', extract_stats.c.request_guid, extract_stats.c.task_id, extract_stats.c.celery_task_id, unique=False)
    return metadata
