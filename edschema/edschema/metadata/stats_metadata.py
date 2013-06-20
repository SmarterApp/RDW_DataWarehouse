'''
Created on Jun 19, 2013

@author: tosako
'''
from sqlalchemy.schema import MetaData, Table, Column, Index
from sqlalchemy.types import String, DateTime, BigInteger

def generate_stats_metadata(schema_name=None, bind=None):
    metadata = MetaData(schema=schema_name, bind=bind)
    udl_stats = Table('udl_stats', metadata,
                        Column('tenant', String(32), primary_key=True),
                        Column('state_code', String(2), primary_key=True),
                        Column('laod_start', DateTime, nullable=False),
                        Column('load_end', DateTime, nullable=False),
                        Column('load_status', String(32), nullable=False),
                        Column('record_loaded_count', BigInteger, nullable=False),
                        Column('last_pdf_generated', DateTime, nullable=False),
                        Column('last_pre_cached', DateTime, nullable=False)
                        )
    Index('udl_stats_idx', udl_stats.c.tenant, udl_stats.c.state_code, unique=True)
    return metadata
