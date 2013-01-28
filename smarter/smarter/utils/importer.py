'''
Created on Jan 28, 2013

@author: aoren
'''
import datetime
import csv
import os
from smarter.utils.connector import DBConnector


def import_from_file(file_path, metadata, connector):

    fileName, fileExtension = os.path.splitext(file_path)

    with open(file_path, newline='') as csvfile:
        total_lines = 0
        line_number = 0
        try:
            start_date = datetime.datetime.now()
            file_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            connector = DBConnector()
            table = connector.get_table(fileName)

            for row in file_reader:
                line_number += 1
                total_lines += 1

                connector.execute(users.insert(), [
                                    {'first_name': "A", 'last_name' : "B"},
                                    {'first_name': "C", 'last_name' : "D"},
                                    {'first_name': "E", 'last_name' : "F"},
                                    {'first_name': "G", 'last_name' : "H"},
                                    ])

            end_date = datetime.datetime.now()
            delta = end_date - start_date
            lines_per_sec = line_number / delta.total_seconds()

            print("Finished file %s (%d lines) in %s (%f lines/sec)" % (file_path, line_number, delta, lines_per_sec))
        except csv.Error as e:
            print('file {}, line {}: {}'.format(file_path, file_reader.line_num, e))

        pass
