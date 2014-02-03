'''
Created on Feb 3rd, 2013

@author: ejen
'''
from sqlalchemy.schema import MetaData, Table, Column
from sqlalchemy.types import String, BigInteger, Text, Integer, Interval, TIMESTAMP
import datetime


def generate_repmgr_metadata(schema_name=None, bind=None):
    metadata = MetaData(schema=schema_name, bind=bind)
    repl_status = Table('repl_status', metadata,
                        Column('primary_node', Integer, primary_key=True),
                        Column('standby_node', Integer, nullable=False),
                        Column('last_wal_primary_location', Text(255), nullable=False),
                        Column('last_wal_standby_location', Text(255), nullable=False),
                        Column('replication_lag', Text(255), nullable=False),
                        Column('apply_lag', Text(255), nullable=False),
                        Column('time_lag', Interval, nullable=False),
                        Column('last_monitor_time', TIMESTAMP, nullable=False, default=datetime.datetime.strptime('20000101000000', '%Y%m%d%H%M%S'))
                        )

    repl_nodes = Table('repl_nodes', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('cluster', Text(255), nullable=False),
                       Column('conninfo', Text(255), nullable=False)
                       )

    return metadata
