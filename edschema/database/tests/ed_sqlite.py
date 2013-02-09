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


# create sqlite from static metadata
def create_sqlite():
    __engine = create_engine('sqlite:///:memory:', connect_args={'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES}, native_datetime=True)
    __metadata = generate_ed_metadata()
    # create tables from static metadata
    __metadata.create_all(__engine)
    # since we want to test db creation, read metadata from sqlite
    __metadata_from_sqlite = MetaData()
    __metadata_from_sqlite.reflect(bind=__engine)
    dbUtil = DbUtil(engine=__engine, metadata=__metadata_from_sqlite)
    component.provideUtility(dbUtil, IDbUtil)


# import data from csv files
def generate_data():
    dbconnector = DBConnector()
    connection = dbconnector.open_connection()
    here = os.path.abspath(os.path.dirname(__file__))
    resources_dir = os.path.join(os.path.join(here, 'resources'))

    # Test data is generated from:
    # https://docs.google.com/folder/d/0B3TkaEXHzX2TcWw3bnVZZDZoVEk/edit?usp=sharing
    # Remember that the order of table insert matters
    resources = ['dim_country',
                 'dim_state',
                 'dim_district',
                 'dim_school',
                 'dim_where_taken',
                 'dim_grade',
                 'dim_student',
                 'dim_teacher',
                 'dim_asmt',
                 'fact_asmt_outcome'
                 ]

    for resource in resources:
        table = dbconnector.get_table(resource)
        with open(os.path.join(resources_dir, resource + ".csv")) as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                new_row = {}
                for field_name in row.keys():
                    clean_field_name = field_name.rstrip()
                    new_row[clean_field_name] = row[field_name]
                connection.execute(table.insert().values(**new_row))
