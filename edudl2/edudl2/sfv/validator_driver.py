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

import argparse
import os

__author__ = 'abrien'

from edudl2.sfv.csv_validator import CsvValidator
from edudl2.sfv.json_validator import JsonValidator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file_path', required=True, type=str, help="Path to the file to be validated.")

    args = parser.parse_args()
    full_file_path = args.file_path
    dir_path = os.path.dirname(full_file_path)
    file_name = os.path.basename(full_file_path)
    file_ext = os.path.splitext(file_name)[1]
    batch_sid = 1

    if file_ext == '.csv':
        validator = CsvValidator()
    elif file_ext == '.json':
        validator = JsonValidator()
    else:
        raise Exception('File must be either csv or json.')
    error_codes = validator.execute(dir_path, file_name, batch_sid)

    for error_code in error_codes:
        print(error_code)


if __name__ == "__main__":
    main()
