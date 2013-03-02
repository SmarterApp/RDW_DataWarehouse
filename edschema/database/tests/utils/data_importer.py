'''
Created on Feb 27, 2013

@author: tosako
'''
from database.connector import DBConnection
from database.tests.utils.data_gen import generate_data


def import_data():
    with DBConnection() as connection:
        generate_data(insert)

        def insert(table_name, rows):
            table = connection.get_table(table_name)
            print(rows)
            connection.execute(table.insert(), rows)
