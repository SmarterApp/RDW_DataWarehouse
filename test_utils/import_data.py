'''
Created on Mar 1, 2013

@author: dip
'''
from database.generic_connector import setup_db_connection_from_ini
import os
from database.data_importer import import_csv_dir
import argparse
import configparser
from database.connector import DBConnection
from edschema.ed_metadata import generate_ed_metadata


def main(config_file, resource_dir):
    '''
    Imports data from csv
    '''
    config = configparser.ConfigParser()
    config.read(config_file)

    metadata = generate_ed_metadata(config.get('app:main', 'edware.schema_name'))
    setup_db_connection_from_ini(config['app:main'], 'edware', metadata)

    delete_data()
    import_csv_dir(resource_dir)


def delete_data():
    '''
    Delete all the data in all the tabls
    '''
    with DBConnection() as connection:
        metadata = connection.get_metadata()
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import csv')
    parser.add_argument('-c', '--config', help='Set the path to ini file')
    parser.add_argument('-r', '--resource', help='Set path to resource directory containing csv')
    args = parser.parse_args()

    __config = args.config
    __resource = args.resource

    parent_dir = os.path.abspath(os.path.join('..', os.path.dirname(__file__)))

    if __config is None:
        __config = os.path.join(os.path.join(parent_dir, 'smarter'), 'test.ini')

    if os.path.exists(__config) is False:
        print('Error: config file does not exist')
        exit(-1)

    if __resource is None:
        __resource = os.path.join(os.path.join(os.path.join(os.path.join(parent_dir, 'edschema'), 'database'), 'tests'), 'resources')

    if os.path.exists(__resource) is False:
        print('Error: resources directory does not exist')
        exit(-1)

    main(__config, __resource)
