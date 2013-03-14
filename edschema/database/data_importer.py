'''
Created on Feb 27, 2013

@author: tosako
'''
from database.connector import DBConnection
import os
import csv
import logging
from sqlalchemy.types import Boolean

logger = logging.getLogger(__name__)


class DataException(Exception):
    '''
    Exception for Data Related problems
    '''
    pass


class DataImporterLengthException(DataException):
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
    if (value is not None and len(value) != 0 or not column.nullable):
        try:
            # need to explicitly convert booleans because they are read from file as strings
            if isinstance(column.type, Boolean):
                if value.lower() == 'true' or value == '1':
                    value = True
                elif value.lower() == 'false' or value == '0':
                    value = False

            value = column.type.python_type(value)
        except:
            msg = 'Cast Exception: Column[%s.%s] value[%s] cast to[%s]' % (column.table.name, column.name, value, column.type.python_type)
            raise DataImporterCastException(msg)
    return value


def __check_data_length(column, value):
    if column.type.python_type == str:
        if column.type.length is not None and column.type.length < len(value):
            msg = 'Length Exception: Column[%s.%s] max length is %d, but the length of value was %d. value[%s]' % (column.table.name, column.name, column.type.length, len(value), value)
            raise DataImporterLengthException(msg)


def __import_csv_file(csv_file, connection, table):
    with open(csv_file) as file_obj:
        # first row of the csv file is the header names
        reader = csv.DictReader(file_obj, delimiter=',')
        for row in reader:
            new_row = {}
            try:
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
            except Exception as x:
                logger.exception(x)
                raise


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
        except Exception as e:
            logging.error("Exception has occured: %s" % e)
            # if there is an error, then roll back
            transaction.rollback()
            __success = False
    return __success
