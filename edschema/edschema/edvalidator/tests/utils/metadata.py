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
Created on Mar 2, 2013

@author: tosako
'''
from sqlalchemy.schema import MetaData, Table, Column
from sqlalchemy.types import SMALLINT, String, Integer, Boolean


def generate_test_metadata(scheme_name=None, bind=None):

    metadata = MetaData(schema=scheme_name, bind=bind)

    table_a = Table('table_a', metadata,
                    Column('row_int_primary', SMALLINT, primary_key=True),
                    Column('row_int', Integer, nullable=False),
                    Column('row_string_5', String(5), nullable=True),
                    )
    table_b = Table('table_b', metadata,
                    Column('row_int_primary', SMALLINT, primary_key=True),
                    Column('row_int', Integer, nullable=False),
                    Column('updated', Boolean, nullable=True),
                    )
    return metadata
