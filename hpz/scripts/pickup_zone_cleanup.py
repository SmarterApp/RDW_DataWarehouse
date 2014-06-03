__author__ = 'smuhit'


import os
import argparse
from datetime import datetime
from datetime import timedelta
from sqlalchemy.sql import select, delete
from sqlalchemy import create_engine, Table
from sqlalchemy.schema import MetaData
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


def cleanup(config_file_path, expiration_duration):
    time_now = datetime.now()
    time_change = timedelta(days=expiration_duration)
    expiration_time = time_now - time_change

    config = ConfigParser()
    config.read(config_file_path)
    db_url = config['app:main']['hpz.db.url']
    db_schema = config['app:main']['hpz.db.schema_name']

    engine = create_engine(db_url)
    metadata = MetaData(schema=db_schema, bind=engine)
    metadata.reflect(schema=db_schema, bind=engine)
    with engine.connect() as conn:
        file_reg_table = Table('file_registry', metadata)
        select_query = select([file_reg_table.c.file_path]).where(file_reg_table.c.create_dt <= expiration_time)
        files_to_delete = conn.execute(select_query).fetchall()
        delete_query = delete(file_reg_table).where(file_reg_table.c.create_dt <= expiration_time)
        conn.execute(delete_query)

    for file_to_delete in files_to_delete:
        if os.path.exists(file_to_delete[0]):
            os.remove(file_to_delete[0])


parser = argparse.ArgumentParser(description='Cleanup HTTP pickup zone files and database')
parser.add_argument('-c', '--config', help="The path to the ini file", default="/opt/edware/conf/hpz.ini")
parser.add_argument('-e', '--expiration', type=int, required=True, help="The expiration time for files (in days)")
args = parser.parse_args()

cleanup(args.config, args.expiration)
