__author__ = 'tshewchuk'

"""
This module defines a simple CSV file writer.
"""

import csv


def write_csv(file, header, data):
    """
    Write the header and data to the specified file in CSV format.
    NOTE: Special characters will be quoted.

    @param file: Directory pathname of CSV file to be written.
    @param header: Header row for CSV file.
    @param data: Data rows for CSV file.
    """

    with open(file, 'w') as csv_file:
        csvwriter = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(header)
        for row in data:
            csvwriter.writerow(row)


def append_csv(file, data):
    """
    Write data to the specified file in CSV format.
    NOTE: This will append to an existing file and does NOT write headers
    NOTE: Special characters will be quoted.

    @param file: Directory pathname of CSV file to be written.
    @param data: Data rows for CSV file.
    """

    with open(file, 'a') as csv_file:
        csvwriter = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        for row in data:
            csvwriter.writerow(row)
