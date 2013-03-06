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


class DataImporterCastException(Exception):
    '''
    Exception for Data Importer Cast
    '''
    pass


def __cast_data_type(column, value):
    '''
    cast value dynamically
    '''
    # if value is not None and length is not 0 AND not nullable
    # get python_type property, then cast
    cast = False
    if (value is not None and len(value) != 0):
        cast = True
    else:
        if not column.nullable:
            cast = True
    if cast:
        try:
            value = column.type.python_type(value)
        except:
            msg = 'Cast Failure [%s.%s]' % (column.table.name, column.name)
            raise DataImporterCastException(msg)
    return value


def __check_data_length(column, value):
    if column.type.python_type == str:
        if column.type.length is not None and column.type.length < len(value):
            msg = 'column[%s.%s] max length is %d, but the length of value was %d. value[%s]' % (column.table.name, column.name, column.type.length, len(value), value)
            raise DataImporterLengthException(msg)


def __import_csv_file(csv_file, connection, table):
    with open(csv_file) as file_obj:
        # first row of the csv file is the header names
        reader = csv.DictReader(file_obj, delimiter=',')
        for row in reader:
            new_row = {}
            for field_name in list(row.keys()):
                # strip out spaces and \n
                clean_field_name = field_name.rstrip()
                value = row[field_name]
                column = table.c[clean_field_name]
                value = __cast_data_type(column, value)
                __check_data_length(column, value)
                new_row[clean_field_name] = value
            # Inserts to the table one row at a time
            connection.execute(table.insert().values(**new_row))


def import_csv_dir(resources_dir, datasource_name=''):
    '''
    import data from csv files
    return
        True: load data successfully
        False: no data loaded or failed to load data
    '''
    __success = False
    with DBConnection(name=datasource_name) as connection:
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
                    __import_csv_file(csv_file=file, connection=connection, table=table)
            # if there is not an error, then commit
            transaction.commit()
        except:
            logging.error("Exception has occured", exc_info=1)
            # if there is an error, then roll back
            transaction.rollback()
            __success = False
    return __success
