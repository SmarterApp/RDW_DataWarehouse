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
Created on Feb 27, 2013

@author: tosako
'''
from edschema.database.connector import DBConnection
from edschema.database.tests.utils.data_gen import generate_data


def import_data():
    with DBConnection() as connection:
        generate_data(insert)

        def insert(table_name, rows):
            table = connection.get_table(table_name)
            print(rows)
            connection.execute(table.insert(), rows)
