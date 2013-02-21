'''
Created on Feb 8, 2013

@author: tosako
'''
import os
from sqlalchemy.engine import create_engine
from database.connector import DbUtil, IDbUtil, DBConnector
from zope import component
from edschema.ed_metadata import generate_ed_metadata
import csv
import sqlite3
from sqlalchemy.schema import MetaData
from database.tests.data_gen import generate_data


# create sqlite from static metadata
def create_sqlite():
    __engine = create_engine('sqlite:///:memory:', connect_args={'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES}, native_datetime=True)
    __metadata = generate_ed_metadata()
    # create tables from static metadata
    __metadata.create_all(bind=__engine, checkfirst=False)
    # since we want to test db creation, read metadata from sqlite
    __metadata_from_sqlite = MetaData()
    __metadata_from_sqlite.reflect(bind=__engine)
    dbUtil = DbUtil(engine=__engine, metadata=__metadata_from_sqlite)
    component.provideUtility(dbUtil, IDbUtil)


# drop tables from memory
def destroy_sqlite():
    dbUtil = component.queryUtility(IDbUtil)
    __engine = dbUtil.get_engine()
    __metadata = dbUtil.get_metadata()
    __metadata.drop_all(bind=__engine, checkfirst=False)
    __engine.dispose()
    component.provideUtility(None, IDbUtil)


def import_data():
    dbconnector = DBConnector()
    connection = dbconnector.open_connection()

    def insert(table_name, rows):
        table = dbconnector.get_table(table_name)
        print(rows)
        connection.execute(table.insert(), rows)
    generate_data(insert)


# import data from csv files
def import_csv_data():
    dbconnector = DBConnector()
    connection = dbconnector.open_connection()
    here = os.path.abspath(os.path.dirname(__file__))
    resources_dir = os.path.join(os.path.join(here, 'resources'))

    # Test data is generated from:
    # https://docs.google.com/folder/d/0B3TkaEXHzX2TcWw3bnVZZDZoVEk/edit?usp=sharing

    # Traverse through the resources directory for .csv files
    # We assume that the name of the file is the name of the table
    for file in os.listdir(resources_dir):
        # splits the path name and the extension
        file_name, file_extension = os.path.splitext(file)
        if (file_extension == '.csv'):
            table = dbconnector.get_table(file_name)
            with open(os.path.join(resources_dir, file)) as file_obj:
                # first row of the csv file is the header names
                reader = csv.DictReader(file_obj, delimiter=',')
                for row in reader:
                    new_row = {}
                    for field_name in row.keys():
                        # strip out spaces and \n
                        clean_field_name = field_name.rstrip()
                        new_row[clean_field_name] = row[field_name]
                    # Inserts to the table one row at a time
                    connection.execute(table.insert().values(**new_row))
