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

import csv
import argparse


def main(csv_file):
    with open(csv_file, encoding='utf-8') as cfile:
        c_reader = csv.reader(cfile)
        for row in c_reader:
            out_str = [empty_str_to_none(val) for val in row]
            print(tuple(out_str), ',', sep='')


def empty_str_to_none(value):
    '''Convert any empty string to None'''
    if value == '':
        return None
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser('csv_to_tup')
    parser.add_argument('-c', '--csv_file', help='name of csv file', required=True)
    args = parser.parse_args()

    main(args.csv_file)
