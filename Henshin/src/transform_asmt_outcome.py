'''
Transform generated assessment outcome data into landing zone format - [Outcome]
Landing Zone Format: https://confluence.wgenhq.net/display/CS/New+UDL
'''
import os.path
import csv
from column_headers import COLUMN_HEADER_INFO

DATAFILE_PATH = str(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
DEFAULT_FACT_ASMT_OUTCOME_FILE = os.path.join(DATAFILE_PATH, 'datafiles', 'fact_asmt_outcome.csv')
DEFAULT_LANDING_ZONE_OUTCOME_FILE = os.path.join(DATAFILE_PATH, 'datafiles', 'METADATA_ASMT_ID_{0}.csv')


def transform_to_realdata(source_file, asmt_id_list, fact_asmt_outcome_file_pattern):
    '''
    Function to transform data from fact_asmt_outcome.csv into landing zone format
    @param source_file: file name/path of input fact_asmt_outcome.csv file
    @param asmt_id_list: all asmt_ids. Each asmt_id maps to one csv file to be generated
    @param output_file_prefix: output file path prefix
    '''
    # check if file exists or not, file type, etc
    is_valid_file = validate_file(source_file)

    # valid file
    if is_valid_file:
        # check if all required columns in target_headers has corresponding column in source_file
        # If it has, get list of target_headers, and corresponding source_headers. Otherwise, throw exception
        target_headers, source_headers = get_source_and_target_headers(source_file)
        if len(target_headers) > 0 and len(target_headers) == len(source_headers):
            # start transformation process
            transform_file_process(source_file, asmt_id_list, target_headers, source_headers, fact_asmt_outcome_file_pattern)


def validate_file(file_name):
    '''
    Validate the input file
    '''
    isValid = os.path.exists(file_name) and os.path.isfile(file_name)
    if isValid is False:
        print("invalid file ", file_name)
    return isValid


def get_source_and_target_headers(source_file):
    '''
    Generate reordered columns in source_file by the given data_layout
    '''
    # flatten the required columns
    target_headers = []
    source_headers = []
    # read headers from source_file
    with open(source_file, newline='') as file:
        reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
        column_names_in_srouce_file = next(reader)

    # loop column_header_info, create target_headers, column_names_in_srouce_file
    for source_and_target_column_mapping in COLUMN_HEADER_INFO:
        target_column_name = source_and_target_column_mapping[0]
        source_column_name = source_and_target_column_mapping[1]

        if source_column_name in column_names_in_srouce_file:
            target_headers.append(target_column_name)
            source_headers.append(source_column_name)
        else:
            print("column missing ", source_column_name)
            raise Exception

    return target_headers, source_headers


def transform_file_process(source_file, asmt_id_list, target_headers, source_headers, fact_asmt_outcome_file_pattern):
    '''
    Transformation process
    '''
    print("Start to transform ", source_file, "into landing zone format...")
    # filter all rows which asmt_id in asmt_id_list
    # transformed_rows_dict is a dictionary. Key is the asmt_id in asmt_id_list, and values are list of rows in source file
    transformed_rows_dict = filter_by_asmt_id(source_file, asmt_id_list, source_headers)

    # create target files
    for asmt_id, rows in transformed_rows_dict.items():
        # output file name format
        output_file = fact_asmt_outcome_file_pattern.format(str(asmt_id))
        with open(output_file, 'w', newline='') as csvfile:
            output_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            # write headers
            output_writer.writerow(target_headers)
            # write rows
            output_writer.writerows(rows)
    print("Done!")


def filter_by_asmt_id(source_file, asmt_id_list, source_headers):
    '''
    Function to filter rows in csv file
    Read source_file, generate a dictionary which
    use column asmt_id as key, corresponding row as one item in value
    '''
    # initialize dictionary
    asmt_dict = {}
    for asmt_id in asmt_id_list:
        asmt_dict[str(asmt_id)] = []

    with open(source_file, newline='') as file:
        reader = csv.DictReader(file, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            asmt_guid = row['asmt_rec_id']
            if asmt_guid in asmt_dict.keys():
                # pick values only in source_headers
                new_row = [row[source_column] for source_column in source_headers]
                asmt_dict[str(asmt_guid)].append(new_row)
    return asmt_dict


if __name__ == '__main__':
    print(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))
    source_file = DEFAULT_FACT_ASMT_OUTCOME_FILE
    target_file_path = DEFAULT_LANDING_ZONE_OUTCOME_FILE
    asmt_id_list = [i for i in range(20, 35)]
    transform_to_realdata(source_file, asmt_id_list, target_file_path)
