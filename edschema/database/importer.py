'''
Created on Jan 28, 2013

@author: aoren
'''
import datetime
import csv
import os


def import_from_file(file_path, connector):

    file_name, file_extension = os.path.splitext(file_path)

    file_name = os.path.basename(file_name)

    if file_extension != '.csv':
        return

    with open(file_path, newline='') as csvfile:
#        total_lines = 0
        line_number = 0
        try:
            start_date = datetime.datetime.now()
            file_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            table = connector.get_table(file_name)
            connection = connector.open_connection()

            dictionaries = []
            # convert rows to dictionaries
            for row in file_reader:
                dictionaries.append(dict((table.columns[k], v) for k, v in row.iteritems()))

#                line_number += 1
#                total_lines += 1

            connection.execute(table.insert(), dictionaries)

            end_date = datetime.datetime.now()
            delta = end_date - start_date
            lines_per_sec = line_number / delta.total_seconds()

            print("Finished file %s (%d lines) in %s (%f lines/sec)" % (file_path, line_number, delta, lines_per_sec))
        except csv.Error as e:
            print('file {}, line {}: {}'.format(file_path, file_reader.line_num, e))
        except Exception as e:
            print(e)
