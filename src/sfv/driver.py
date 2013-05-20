#!/usr/bin/env python

import argparse
import os

__author__ = 'abrien'

from sfv.csv_validator import CsvValidator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file_path', required=True, type=str, help="Path to the file to be validated.")

    args = parser.parse_args()
    full_file_path = args.file_path
    dir_path = os.path.dirname(full_file_path)
    file_name = os.path.basename(full_file_path)
    batch_sid = 1

    validator = CsvValidator()
    error_codes = validator.execute(dir_path, file_name, batch_sid)

    for error_code in error_codes:
        print(error_code)



if __name__ == "__main__":
    main()