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
from smarter.database.datasource import get_datasource_name,\
    parse_db_settings, get_db_config_prefix


def main(config_file, resource_dir):
    '''
    Imports data from csv
    '''
    config = configparser.ConfigParser()
    config.read(config_file)

    tenants, db_options = parse_db_settings(config['app:main'])
    for tenant in tenants:
        prefix = get_db_config_prefix(tenant)
        schema_key = prefix + 'schema_name'
        metadata = generate_ed_metadata(db_options[schema_key])
        # Pop schema name as sqlalchemy doesn't like db.schema_name being passed
        db_options.pop(schema_key)
        datasource_name = get_datasource_name(tenant)
        setup_db_connection_from_ini(db_options, prefix, metadata, datasource_name=datasource_name)

        delete_data(get_datasource_name(tenant))
        import_csv_dir(resource_dir, datasource_name )


def delete_data(name):
    '''
    Delete all the data in all the tabls
    '''
    with DBConnection(name) as connection:
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
