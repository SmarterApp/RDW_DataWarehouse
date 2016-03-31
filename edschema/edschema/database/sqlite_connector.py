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
Created on Feb 8, 2013

@author: tosako
'''
from sqlalchemy.engine import create_engine
from edschema.database.connector import DbUtil, IDbUtil
from zope import component
from edschema.metadata.ed_metadata import generate_ed_metadata
import sqlite3
from sqlalchemy.schema import MetaData
from sqlalchemy import event
import traceback


# create sqlite from static metadata
def create_sqlite(force_foreign_keys=True, use_metadata_from_db=False, echo=False, metadata=None, datasource_name=''):
    __engine = create_engine('sqlite:///:memory:', connect_args={'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES}, native_datetime=True, echo=echo)

    if force_foreign_keys:
        event.listen(__engine, 'connect', __fk_on)

    __metadata = metadata
    if __metadata is None:
        __metadata = generate_ed_metadata()
    # create tables from static metadata
    __metadata.create_all(bind=__engine, checkfirst=False)

    if use_metadata_from_db:
        # since we want to test db creation, read metadata from sqlite
        __metadata = MetaData()
        __metadata.reflect(bind=__engine)

    dbUtil = DbUtil(engine=__engine, metadata=__metadata)
    component.provideUtility(dbUtil, IDbUtil, name=datasource_name)


def __fk_on(connection, rec):
    connection.execute('pragma foreign_keys=ON')


def destroy_sqlite(datasource_name=''):
    '''
    drop tables from memory
    and destory sqlite
    @param datasource_name: the datasource name
    @type datasource_name: string
    '''
    dbUtil = component.queryUtility(IDbUtil, name=datasource_name)
    __engine = dbUtil.get_engine()
    __metadata = dbUtil.get_metadata()
    __metadata.drop_all(bind=__engine, checkfirst=False)
    __engine.dispose()
    component.provideUtility(None, IDbUtil)
