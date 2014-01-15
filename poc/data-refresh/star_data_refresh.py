'''
Created on Jan 14, 2014

@author: sravi
'''

from database.generic_connector import setup_db_connection_from_ini
import os
from database.data_importer import import_csv_dir
import argparse
from sqlalchemy import Table, Column, select, MetaData
from sqlalchemy.engine import create_engine
import configparser
from database.connector import DBConnection
from edschema.metadata.ed_metadata import generate_ed_metadata
from edcore.database import get_data_source_names
from edcore.database import initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection


TMP_STG_FACT_TABLE = 'edware_ca_1_3.tmp_fact_asmt_outcome'


def main(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    initialize_db(EdCoreDBConnection, config['app:main'])
    migrate_data()


def connect_db(db_driver, db_user, db_password, db_host, db_port, db_name):
    db_string = '{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'.format(db_driver=db_driver,
                                                                                             db_user=db_user,
                                                                                             db_password=db_password,
                                                                                             db_host=db_host,
                                                                                             db_port=db_port,
                                                                                             db_name=db_name)
    # print(db_string)
    engine = create_engine(db_string)
    db_connection = engine.connect()
    return db_connection, engine


def get_schema_metadata(db_engine, schema_name=None):
    metadata = MetaData()
    metadata.reflect(db_engine, schema_name)
    return metadata


def get_sqlalch_table_object(db_engine, schema_name, table_name):
    metadata = get_schema_metadata(db_engine, schema_name)
    table = metadata.tables[schema_name + '.' + table_name]
    return table


def migrate_fact(connection, source_table, dest_table):
    print('migrating fact from: ' + source_table + ' to ' + str(dest_table))
    fao_tab = select([dest_table])
    result = connection.execute(fao_tab)
    row = result.fetchone()
    print(row)
    pass


def migrate_data():
    '''
    migrate all the data from staging to live star schema fact table
    '''
    connection, engine = connect_db('postgresql+psycopg2', 'edware', 'edware2013', 'dbpgudl0.qa.dum.edwdc.net', 5432, 'edware')
    metadata = get_schema_metadata(engine, 'edware_ca_1_3')
    print(metadata.tables.keys())

    #for dest_table in reversed(metadata.sorted_tables):
    #    print(dest_table)
    #    if 'fact_asmt_outcome' in str(dest_table):
    #        migrate_fact(connection, TMP_STG_FACT_TABLE, dest_table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Refresh')
    parser.add_argument('-c', '--config', help='Set the path to ini file')
    args = parser.parse_args()

    __config = args.config

    if os.path.exists(__config) is False:
        print('Error: config file does not exist')
        exit(-1)

    main(__config)
