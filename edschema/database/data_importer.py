'''
Created on Feb 27, 2013

@author: tosako
'''
from database.connector import DBConnection
import os
import csv
import logging


logger = logging.getLogger(__name__)


class DataImporterLengthException(Exception):
    '''
    Exception for Data Importer
    '''
    pass


def __cast_data_type(data_type, value):
    '''
    cast value dynamically
    '''
    # get python_type property, then cast
    return data_type.python_type(value)


def __check_data_length(data_type, value):
    if data_type.python_type == str:
        if data_type.length is not None and data_type.length < len(value):
            msg = 'max length is %d, but the length of value was %d' % (data_type.length, len(value))
            raise DataImporterLengthException(msg)


def __import_csv_file(csv_file, connection, table):
    with open(csv_file) as file_obj:
        # first row of the csv file is the header names
        reader = csv.DictReader(file_obj, delimiter=',')
        for row in reader:
            new_row = {}
            for field_name in row.keys():
                # strip out spaces and \n
                clean_field_name = field_name.rstrip()
                value = row[field_name]
                column_type = table.c[clean_field_name].type
                value = __cast_data_type(column_type, value)
                __check_data_length(column_type, value)
                new_row[clean_field_name] = value
            # Inserts to the table one row at a time
            connection.execute(table.insert().values(**new_row))


def import_csv_dir(resources_dir, name=''):
    '''
    import data from csv files
    return
        True: load data successfully
        False: no data loaded or failed to load data
    '''
    __success = False
    with DBConnection(name=name) as connection:
        metadata = connection.get_metadata()
        # Look through metadata and upload available imports with the same and and ext csv
        # use transaction.
        # if importing is okay. then commit the transaction; otherwise, roll back
        transaction = connection.get_connection().begin()
        try:
            for table in metadata.sorted_tables:
                file = os.path.join(resources_dir, table.name + '.csv')
                # if import exists, upload it
                if os.path.exists(file):
                    # Found csv file.  set it True
                    __success = True
                    __import_csv_file(file, connection, table)
            # if there is not an error, then commit
            transaction.commit()
        except:
            logging.error("Exception has occured", exc_info=1)
            # if there is an error, then roll back
            transaction.rollback()
            __success = False
    return __success
