# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

"""
This module defines a simple CSV file writer.
"""

import csv


def write_csv(file_object, rows, header=None, delimiter=','):
    """
    Write the header and data to the specified file in CSV format.
    NOTE: Special characters will be quoted.

    @param file: Directory pathname of CSV file to be written.
    @param header: Header row for CSV file.
    @param rows: Data rows for CSV file.
    """
    csvwriter = csv.writer(file_object, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
    if header is not None:
        csvwriter.writerow(header)
    csvwriter.writerows(rows)
    return True
