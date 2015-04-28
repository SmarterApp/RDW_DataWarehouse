'''
Created on Apr 27, 2015

@author: tosako
'''
import os
from datetime import datetime, timedelta
from sqlalchemy.sql import select, delete
from sqlalchemy.sql.expression import bindparam
from hpz.database.hpz_connector import HPZDBConnection


def cleanup(expiration_duration):
    time_now = datetime.now()
    if type(expiration_duration) is str:
        expiration_duration = int(expiration_duration)
    time_change = timedelta(days=expiration_duration)
    expiration_time = time_now - time_change

    with HPZDBConnection() as conn:
        file_reg_table = conn.get_table('file_registry')

        select_query = select([file_reg_table.c.registration_id, file_reg_table.c.file_path])\
            .where(file_reg_table.c.create_dt <= expiration_time)
        delete_query = delete(file_reg_table).where(file_reg_table.c.registration_id == bindparam('registration_id'))

        results = conn.execute(select_query, stream_results=True)
        rows = results.fetchmany(1024)
        while len(rows) > 0:
            for row in rows:
                if os.path.exists(row['file_path']):
                    os.remove(row['file_path'])

                conn.execute(delete_query, registration_id=row['registration_id'])
            rows = results.fetchmany(1024)
