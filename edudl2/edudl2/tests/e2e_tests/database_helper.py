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
Created on Mar 19, 2014

@author: dip
'''
from sqlalchemy.schema import DropSchema
from edudl2.database.udl2_connector import get_target_connection


def drop_target_schema(tenant, schema_name):
    with get_target_connection(tenant) as connector:
        try:
            connector.execute(DropSchema(schema_name, cascade=True))
        except:
            pass
