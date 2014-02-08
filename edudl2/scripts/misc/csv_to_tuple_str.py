import csv
import argparse


def main(csv_file):
    with open(csv_file) as cfile:
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
