import csv
from argparse import ArgumentParser


def parse():
    parser = ArgumentParser(prog='csv stretcher',
                            description="Read a valid CSV file. Multiply number of rows or columns and write them to output CSV file",
                            epilog="ex: python3.3 ElasticCsv.py -r 2 -c 2 -s small.csv -o big.csv, this reads small.csv and double number of rows and number of columns by repeated the small csv block. the it write the csv to big.csv")
    parser.add_argument('-r', dest='row_multiplier', type=int, default=1, help="times of rows to be muliplied")
    parser.add_argument('-c', dest='column_multiplier', type=int, default=1, help="times of columns to be multiplied")
    parser.add_argument('-s', dest='source_csv', required=True, help="path and file name to the csv file for input")
    parser.add_argument('-o', dest='output_data_csv', required=True, help="path and file name to the csv file of output data")
    parser.add_argument('-m', dest='output_metadata_csv', default=2, help="path and file name to csv file of metadata for output")
    parser.add_argument('-t', dest='apply_transformation_rules', default='True', help="apply transformation rules or not")

    args = parser.parse_args()
    # print(args)
    conf = {'row_multiplier': args.row_multiplier,
            'column_multiplier': args.column_multiplier,
            'source_csv': args.source_csv,
            'output_data_csv': args.output_data_csv,
            'output_metadata_csv': args.output_metadata_csv,
            'apply_transformation_rules': args.apply_transformation_rules}

    return conf


def read_source_csv(csv_file, header_row_count):
    # print('Read csv from source file %s' % csv_file)
    rows = []
    with open(csv_file) as csv_file_obj:
        csv_reader = csv.reader(csv_file_obj)
        for row in csv_reader:
            rows.append(row)
    csv_obj = {'header': [], 'rows': []}
    try:
        if header_row_count == 3:
            (csv_obj['header'], csv_obj['metadata'], csv_obj['rows']) = (rows[1], rows[2], rows[3:])
        elif header_row_count == 2:
            (csv_obj['header'], csv_obj['metadata'], csv_obj['rows']) = (rows[1], ['text'] * len(rows[1]), rows[2:])
        else:
            raise csv.Error("data file's header count is not in documented range. Please corret csv input file or update ElasticCsv.py to handle it")
    except Exception as e:
        print(e)
    return csv_obj


def multiply_header_by_column(header, multiplier=1):
    result_header = [i + (' ' + str(j + 1) if j > 0 else '') for j in range(0, multiplier) for i in header]
    return result_header


def multiply_metadata_by_column(metadata, multiplier=1):
    result_metadata = [i for j in range(0, multiplier) for i in metadata]
    return result_metadata


def multiply_rows_by_column(rows, multiplier=1):
    result = [[r for i in range(0, multiplier) for r in row] for row in rows ]
    return result


def multiply_rows_by_row(rows, multiplier=1):
    result = [row for i in range(0, multiplier) for row in rows]
    return result


def stretch_csv(source_csv_obj, row_multiplier=1, column_multiplier=1):
    # print('Strech csv by %s times rows and %s times columns' % (row_multiplier, column_multiplier))
    # print(input_csv_obj)
    output_csv_obj = {'header': [], 'metadata': [], 'rows': []}
    # Multiply headers
    output_csv_obj['header'] = multiply_header_by_column(source_csv_obj['header'], column_multiplier)
    # Multiply metadata
    output_csv_obj['metadata'] = multiply_metadata_by_column(source_csv_obj['metadata'], column_multiplier)
    # Multiply rows
    output_csv_obj['rows'] = multiply_rows_by_row(multiply_rows_by_column(source_csv_obj['rows'], column_multiplier), row_multiplier)
    return output_csv_obj


def write_streched_data_csv(csv_obj, output_data_csv):
    # print('Writing Streched data CSV to %s' % output_data_csv)
    with open(output_data_csv, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_obj['header'])
        for i in csv_obj['rows']:
            csv_writer.writerow(i)


def write_streched_metadata_csv(csv_obj, output_metadata_csv):
    # print('Wriring Streched metadata CSV to %s', output_metadata_csv)
    columns = [i for i in zip(csv_obj['header'], csv_obj['metadata'])]
    with open(output_metadata_csv, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['column Name', 'column Type'])
        for i in columns:
            csv_writer.writerow([i[0], i[1]])


def check_input_output_conflic(source_csv, output_data_csv, output_metadata_csv):
    # need more sophisticated checks due to path travesals can break this, or symlink
    return (source_csv == output_data_csv) or (source_csv == output_metadata_csv) or (output_data_csv == output_metadata_csv)


def check_multiplier_greater_than_zero(multiplier):
    return multiplier > 0


def get_header_row_count(source_csv):
    # this check is very fragile. It assumes Header Row Count exists and use Header-Row-Count to skip headers.
    # and it assumes row 3 is metadata
    # print('check header row count and decide metadata existence')
    header_row_count = None
    with open(source_csv, 'r') as csv_file_obj:
        csv_reader = csv.reader(csv_file_obj)
        counter = 0
        header_row_count
        for row in csv_reader:
            if counter == 0:
                header_row_count = int(row[1])
                break
            else:
                break
    return header_row_count


if __name__ == '__main__':
    conf = parse()
    if check_input_output_conflic(conf['source_csv'], conf['output_data_csv'], conf['output_metadata_csv']):
        print("input csv file, output data csv file and output metadata csv file must be all different")
        exit()
    if not check_multiplier_greater_than_zero(conf['row_multiplier']):
        print("row multiplier must be greater than zero")
        exit()
    if not check_multiplier_greater_than_zero(conf['column_multiplier']):
        print("column multiplier must be greater than zero")
        exit()

    header_row_count = get_header_row_count(conf['source_csv'])
    input_csv_obj = read_source_csv(conf['source_csv'], header_row_count)

    output_csv_obj = stretch_csv(input_csv_obj, conf['row_multiplier'], conf['column_multiplier'])
    write_streched_data_csv(output_csv_obj, conf['output_data_csv'])
    write_streched_metadata_csv(output_csv_obj, conf['output_metadata_csv'])
