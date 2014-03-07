import os
import csv
import math
import itertools
from uuid import uuid4
from edudl2.udl2_util.file_util import create_directory


def validate_file(file_name):
    '''
    Simple validation that file exists
    TODO:  we might need to do more validation for csv,
    '''
    return False if not (os.path.exists(file_name) and os.path.isfile(file_name)) or os.path.getsize(file_name) <= 0 else True


def split_file(file_name, delimiter=',', row_limit=10000, parts=0, output_dir='./'):
    '''
    Split files into either parts or row limit so we can process smaller files
    Precedence of parts over row_limit when both are supplied
    '''
    if not validate_file(file_name):
        raise Exception('Unable to split invalid file')
    create_directory(output_dir)

    with open(file_name) as csvfile:
        data = csv.reader(csvfile, delimiter=delimiter)
        header = next(data)
        total_rows = 0
        # Get the total number of records
        for row in data:
            total_rows += 1
        if total_rows is 0:
            raise Exception('CSV file has no data')
        if parts is 0:
            parts = math.ceil(total_rows / row_limit)
        # Recalculate values
        row_limit = math.ceil(total_rows / parts)
        parts = math.ceil(total_rows / row_limit)
        # Split files
        split_file_list = []
        for i in range(1, parts + 1):
            csvfile.seek(0)
            # Generate file names that will be loaded into fdw
            output_file = os.path.join(output_dir, 'part_' + str(uuid4()) + '.csv')
            with open(output_file, 'w') as writerfile:
                row_count = 0
                start = row_limit * (i - 1) + 1
                end = i * row_limit + 1
                # Slice the iterator based on start and end
                for row in itertools.islice(data, start, end):
                    csvwriter = csv.writer(writerfile, delimiter=delimiter)
                    csvwriter.writerow(row)
                    row_count += 1
                split_file_list.append([output_file, row_count, start])

    # save headers to output dir
    header_path = os.path.join(output_dir, 'headers.csv')
    with open(header_path, 'w') as csv_header_file:
        header_writer = csv.writer(csv_header_file, delimiter=delimiter)
        header_writer.writerow(header)
        csv_header_file.flush()  # EJ, make sure the file is writtend into disk. this happens only when benchmark prints frames

    return split_file_list, header_path, total_rows, os.path.getsize(file_name)
