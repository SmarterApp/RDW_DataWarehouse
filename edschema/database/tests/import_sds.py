'''
Created on Mar 1, 2013

@author: dip
'''
from database.generic_connector import setup_connection
import os
from database.data_importer import import_csv_dir
import argparse
import configparser
from database.connector import DBConnection


def main(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    schema_name = config.get('app:main', 'edschema.schema_name')
    setup_connection(config['app:main'], 'edware.db.main.', schema_name)
    here = os.path.abspath(os.path.dirname(__file__))
    resources_dir = os.path.join(os.path.join(here, 'resources'))
    delete_data()
    import_csv_dir(resources_dir)


def delete_data():
    with DBConnection() as connection:
        metadata = connection.get_metadata()
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import csv')
    parser.add_argument('-config', help='Set the path to ini file')
    parser.add_argument('--resource', help='Set path to resource file')
    args = parser.parse_args()
    
    __config = args.config
    __resource = args.resource
    
    if __config is None:
        print('Please specify path to ini file')
        exit(-1)
    
    main(args.config)
    