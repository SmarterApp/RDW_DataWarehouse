'''
Created on Jan 28, 2013

@author: aoren
'''
import datetime
import csv
import os
from collections import Counter
from sqlalchemy.sql.expression import func, select


def import_from_file(file_path, connector):

    file_name, file_extension = os.path.splitext(file_path)

    file_name = os.path.basename(file_name)

    if file_extension != '.csv':
        return

    with open(file_path, newline='') as csvfile:
        line_number = 0
        try:
            start_date = datetime.datetime.now()
            file_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            table = connector.get_table(file_name)
            connection = connector.open_connection()

            dictionaries = []
            column_list = [c.name for c in table.columns]
            # convert rows to dictionaries

            try:
                result = connection.execute(select([func.count(list(table.c)[0]).label('my_count')]))
                index = result.fetchone()['my_count']
                for row in file_reader:
                    index = index + 1
                    row.insert(0, index)
                    dictionary = dict(zip(column_list, row))
                    dictionaries.append(dictionary)
            except Exception as e:
                print(e)

            connection.execute(table.insert(), dictionaries)

            end_date = datetime.datetime.now()
            delta = end_date - start_date
            lines_per_sec = line_number / delta.total_seconds()

            print("Finished file %s (%d lines) in %s (%f lines/sec)" % (file_path, line_number, delta, lines_per_sec))
        except csv.Error as e:
            print('file {}, line {}: {}'.format(file_path, file_reader.line_num, e))
        except Exception as e:
            print(e)
