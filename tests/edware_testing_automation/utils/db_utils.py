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

"""
Created on Feb 22, 2013

@author: dip
"""
import csv
import os

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import select
from zope.component.globalregistry import provideUtility

from edware_testing_automation.utils.db_connector import DbUtil, IDbUtil, DBConnection


def create_connection(url, schema_name, datasource_name=''):
    __engine = create_engine(url)

    __metadata = MetaData(schema=schema_name, bind=__engine)
    __metadata.reflect(schema=schema_name, bind=__engine)

    dbUtil = DbUtil(engine=__engine, metadata=__metadata)
    provideUtility(dbUtil, IDbUtil, name=datasource_name)


# import data from csv files
def import_long_live_sessions(schema_name, datasource_name=''):
    with DBConnection(name=datasource_name) as connector:
        user_session = connector.get_table('user_session')
        here = os.path.abspath(os.path.dirname(__file__))
        resources_dir = os.path.join(os.path.join(here, 'resources'))
        with open(os.path.join(resources_dir, 'long_lived_sessions.csv')) as file_obj:
            # first row of the csv file is the header names
            reader = csv.DictReader(file_obj, delimiter=',')
            for row in reader:
                new_row = {}
                for field_name in row.keys():
                    # strip out spaces and \n
                    clean_field_name = field_name.rstrip()
                    new_row[clean_field_name] = row[field_name]

                # Inserts to the table one row at a time
                check_existing = connector.get_result(
                    select([user_session.c.session_id], from_obj=[user_session]).where(
                        user_session.c.session_id == new_row['session_id']))
                if len(check_existing) == 0:
                    connector.execute(user_session.insert().values(**new_row))
                else:
                    connector.execute(user_session.update().
                                      values(session_context=new_row['session_context'],
                                             last_access=new_row['last_access'], expiration=new_row['expiration']).
                                      where(user_session.c.session_id == new_row['session_id']))
