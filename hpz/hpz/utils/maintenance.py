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
Created on Apr 27, 2015

@author: tosako
'''
import os
from datetime import datetime, timedelta
from sqlalchemy.sql import select, delete
from sqlalchemy.sql.expression import bindparam
from hpz.database.hpz_connector import HPZDBConnection


def cleanup(settings):
    expiration_duration = settings.get('hpz.record_expiration', 30)
    if type(expiration_duration) is str:
        expiration_duration = int(expiration_duration)
    time_now = datetime.now()
    time_change = timedelta(days=expiration_duration)
    expiration_time = time_now - time_change

    with HPZDBConnection() as conn:
        file_reg_table = conn.get_table('file_registry')
        select_query = select([file_reg_table.c.registration_id, file_reg_table.c.file_path])\
            .where(file_reg_table.c.create_dt <= expiration_time)

        results = conn.execute(select_query, stream_results=True)
        rows = results.fetchall()
        registration_ids = []
        for row in rows:
            if os.path.exists(row['file_path']):
                os.remove(row['file_path'])
            registration_ids.append(row['registration_id'])
        conn.execute(file_reg_table.delete().where(file_reg_table.c.registration_id.in_(registration_ids)))
