__author__ = 'tshewchuk'

"""
This module defines a simple CSV file writer.
"""

import csv


def write_csv(file, rows, header=None, delimiter=','):
    """
    Write the header and data to the specified file in CSV format.
    NOTE: Special characters will be quoted.

    @param file: Directory pathname of CSV file to be written.
    @param header: Header row for CSV file.
    @param rows: Data rows for CSV file.
    """
    written=False
    with open(file, 'w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        if header is not None:
            csvwriter.writerow(header)
        csvwriter.writerows(rows)
        written=True
    return written
