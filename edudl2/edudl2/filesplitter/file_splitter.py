import os
import csv
import math
import itertools


def create_output_destination(file_name, output_path):
    # create output template from supplied input file path
    base = os.path.splitext(os.path.basename(file_name))[0]
    # TODO:  We shouldn't use the base name, use something shorter in length "part.1" or so
    output_name_template = (base + '_part_').replace(' ', '')

    # create output directory
    output_dir = output_path
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_name_template, output_dir


def check_file_size(file_name):
    file_size = os.path.getsize(file_name)
    if file_size <= 0:
        raise Exception('Unable to split, file has size of zero')


def split_file(file_name, delimiter=',', row_limit=10000, parts=0, output_path='./'):
    '''
    Split files into either parts or row limit
    # TODO:  Figure out why we have to send a a list of a list back and the importance of the row
    '''
    isValid = os.path.exists(file_name) and os.path.isfile(file_name)
    if isValid is False:
        raise Exception('File not found!')
    check_file_size(file_name)
    output_name_template, output_dir = create_output_destination(file_name, output_path)

    with open(file_name) as csvfile:
        data = csv.reader(csvfile, delimiter=delimiter)
        header = next(data)
        total_rows = 0
        for row in data:
            total_rows += 1
        if parts is 0:
            parts = math.ceil(total_rows / row_limit)
        row_limit = math.ceil(total_rows / parts)
        # Split files
        split_file_list = []
        for i in range(1, parts + 1):
            csvfile.seek(0)
            output_file = os.path.join(output_dir, output_name_template + str(i) + '.csv')
            with open(output_file, 'w') as writerfile:
                row_count = 0
                start = row_limit * (i - 1) + 1
                end = i * row_limit + 1
                for row in itertools.islice(data, start, end):
                    csvwriter = csv.writer(writerfile, delimiter=',')
                    csvwriter.writerow(row)
                    row_count += 1
                split_file_list.append([output_file, row_count, start])
            # TODO: what is the significance of filesize?
            if i is 1:
                file_size = os.path.getsize(output_file)

    # save headers to output dir
    header_path = os.path.join(output_dir, 'headers.csv')
    with open(header_path, 'w') as csv_header_file:
        header_writer = csv.writer(csv_header_file, delimiter=delimiter)
        header_writer.writerow(header)
        csv_header_file.flush()  # EJ, make sure the file is writtend into disk. this happens only when benchmark prints frames

    return split_file_list, header_path, total_rows, file_size
