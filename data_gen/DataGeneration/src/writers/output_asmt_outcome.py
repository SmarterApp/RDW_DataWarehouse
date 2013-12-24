__author__ = 'swimberly'
import csv
import os

CSV_K = 'csv'


def initialize_csv_file(output_config, output_keys, output_path):
    """
    Given the output configuration dictionary create the corresponding csv files
    :param output_config: A dictionary of configuration information
    :param output_keys: A list of output formats that should be initialized
        these strings must be the top level keys in the output config dictionary
    :return:
    """
    output_files = {}
    for out_key in output_keys:
        csv_info = output_config[out_key].get(CSV_K)
        for table in csv_info:
            file_name = os.path.join(output_path, table + '.csv')
            output_files[table] = file_name
            columns = list(csv_info[table].keys())
            with open(file_name, 'w') as fp:
                csv_writer = csv.writer(fp)
                csv_writer.writerow(columns)

    return output_files


def output_data(output_config, output_keys, output_files, **data):
    """

    :param output_config: The output configuration dictionary
    :param output_keys:
    :param output_files:
    :param data:
    :return:
    """
    pass


if __name__ == '__main__':
    conf_dict = {
        'star': {
            'csv': {
                'fact_asmt_outcome': {
                    'key1': 'asmt_claim_3_score_range_min',
                    'key2': 'asmt_claim_1_score_range_min',
                    'key3': 'asmt_year',
                },
                'dim_student': {
                    'key4': 'blah',
                    'key5': 'blah2',
                }
            }
        }
    }

    out_keys = ['star']
    out_path = os.getcwd()
    print(initialize_csv_file(conf_dict, out_keys, out_path))