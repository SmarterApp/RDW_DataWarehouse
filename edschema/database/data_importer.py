'''
Created on Feb 27, 2013

@author: tosako
'''
from database.connector import DBConnection
import os
import csv


def import_csv_file(csv_file, connection, table):
    with open(csv_file) as file_obj:
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


# import data from csv files
def import_csv_dir(resources_dir):

    with DBConnection() as connection:
        metadata = connection.get_metadata()
        # Look through metadata and upload available imports with the same and and ext csv
        for table in metadata.sorted_tables:
            file = os.path.join(resources_dir, table.name + '.csv')

            # if import exists, upload it
            if os.path.exists(file):
                import_csv_file(file, connection, table)
