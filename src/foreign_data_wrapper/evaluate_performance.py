from elastic_csv.elastic_csv import parse, check_input_output_conflict, check_multiplier_greater_than_zero, read_source_csv, \
    stretch_csv, get_header_row_count, write_stretched_data_csv, write_stretched_metadata_csv
from foreign_data_wrapper.FdwCsvLoader import test_import
import datetime
import os

NUM_OF_ROW_BASE = 100


def get_one_scaled_csv(row_multiplier):
    conf = parse()
    conf['row_multiplier'] = int(row_multiplier)
    if check_input_output_conflict(conf['source_csv'], conf['output_data_csv'], conf['output_metadata_csv']):
        print("input csv file, output data csv file and output metadata csv file must be all different")
        exit()
    if not check_multiplier_greater_than_zero(conf['row_multiplier']):
        print("row multiplier must be greater than zero")
        exit()
    if not check_multiplier_greater_than_zero(conf['column_multiplier']):
        print("column multiplier must be greater than zero")
        exit()
    if not check_boolean_value(conf['apply_transformation_rules']):
        print("apply_transformation_rules must be either True or False")
        exit()
    # set file path
    conf['source_csv'] = os.path.join(os.getcwd(), conf['source_csv'])
    conf['output_data_csv'] = os.path.join(os.getcwd(), conf['output_data_csv'])
    conf['output_metadata_csv'] = os.path.join(os.getcwd(), conf['output_metadata_csv'])
    start_time = datetime.datetime.now()

    header_row_count = get_header_row_count(conf['source_csv'])
    input_csv_obj = read_source_csv(conf['source_csv'], header_row_count)
    output_csv_obj = stretch_csv(input_csv_obj, conf['row_multiplier'], conf['column_multiplier'])
    write_stretched_data_csv(output_csv_obj, conf['output_data_csv'])
    write_stretched_metadata_csv(output_csv_obj, conf['output_metadata_csv'])

    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time for replicating file --", spend_time)

    return conf, spend_time


def check_boolean_value(value):
    if value.lower() in ['true', 'false']:
        return True
    return False


def start_loading_files():
    time_array = []
    # set four rounds
    rounds = [1, 10, 100, 1000, 10000]
    for round in rounds:
        conf, time_for_replicate = get_one_scaled_csv(round)
        time_for_load = start_load_one_file(conf)

        num_of_records = round * NUM_OF_ROW_BASE
        time_as_seconds = float(time_for_load.seconds + time_for_load.microseconds / 1000000.0)
        time_array.append([num_of_records,
                        time_as_seconds,
                        str(time_for_load)])
    print('\nRecords(actual)   Time(seconds)')
    for result in time_array:
        print(result[0], '\t\t', result[1])


def start_load_one_file(conf):
    # start load the file
    # generated replicated data file is input csv file for loading
    # generated meta data file is input metadata file for loading
    conf['csv_file'] = conf['output_data_csv']
    conf['metadata_file'] = conf['output_metadata_csv']
    conf['db_host'] = 'localhost'
    conf['db_port'] = '5432'
    conf['db_user'] = 'postgres'
    conf['db_name'] = 'fdw_test'
    conf['db_password'] = '3423346'
    conf['csv_schema'] = 'public'
    conf['csv_table'] = 'csv_table'
    conf['fdw_server'] = 'udl_import'
    conf['staging_schema'] = 'public'
    conf['staging_table'] = 'tmp'

    time_for_load = test_import(conf)
    return time_for_load


if __name__ == '__main__':
    start_loading_files()
