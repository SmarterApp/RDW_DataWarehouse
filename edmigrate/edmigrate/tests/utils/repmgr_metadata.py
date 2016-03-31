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
Created on Feb 3rd, 2013

@author: ejen
'''
from sqlalchemy.schema import MetaData, Table, Column
from sqlalchemy.types import Text, Integer, Interval, DateTime
import datetime


#
# Note: This schema is not for generation of postgres's repmgr related tables. this is only used for unit test to
# use sqlite to mock real databae.
#
def generate_repmgr_metadata(schema_name=None, bind=None):
    metadata = MetaData(schema=schema_name, bind=bind)
    repl_status = Table('repl_status', metadata,
                        Column('primary_node', Integer, nullable=False),
                        Column('standby_node', Integer, nullable=False),
                        Column('last_wal_primary_location', Text(255), nullable=False),
                        Column('last_wal_standby_location', Text(255), nullable=False),
                        Column('replication_lag', Text(255), nullable=False),
                        Column('apply_lag', Text(255), nullable=False),
                        Column('communication_time_lag', Interval, nullable=False, default=datetime.timedelta(0)),
                        Column('last_monitor_time', DateTime(True), nullable=False, default=datetime.datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
                        )

    repl_nodes = Table('repl_nodes', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('cluster', Text(255), nullable=False),
                       Column('name', Text(255), nullable=False),
                       Column('conninfo', Text(255), nullable=False)
                       )

    return metadata
