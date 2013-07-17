from udl2.W_file_splitter import task
import argparse
import os
from udl2.celery import FILE_SPLITTER_CONF


def main():
    # get parameters from command lines
    parm = get_parameters()

    # verify input parameters
    try:
        if parm['parts'] < 0:
            print("The value for parts should be a positive integer")
            exit()
        if parm['row_limit'] < 0:
            print("The value for number of rows should be a positive integer")
            exit()
        if not is_valid_file(parm['input_file']):
            print('The input file is invalid')
            exit()
        if not os.path.isdir(parm['output_path']):
            os.makedirs(parm['output_path'])

    except Exception as e:
        print(e)
    # execute the file_splitter task
    split_file_result = task.apply_async([parm], queue='Q_files_to_be_split')
    print("Status", split_file_result.status)
    print("Result", split_file_result.get())


def get_parameters():
    '''
    Returns parameters from command line as a dictionary
    '''

    # default values for the arguments are defined in FILE_SPLITTER_CONF
    parser = argparse.ArgumentParser(description='File Splitter Worker')
    parser.add_argument("-p", "--parts", type=int, default=FILE_SPLITTER_CONF['parts'], help="number of parts to be split")
    parser.add_argument("-r", "--row_limit", type=int, default=FILE_SPLITTER_CONF['row_limit'], help="number of rows in each sub file")
    parser.add_argument("-i", "--input_file", required=True, help="input file")
    parser.add_argument("-o", "--output_path", default=FILE_SPLITTER_CONF['output_path'], help="output directory")
    args = parser.parse_args()
    conf = {'parts': args.parts,
            'row_limit': args.row_limit,
            'input_file': args.input_file,
            'output_path': args.output_path,
            'keep_headers': FILE_SPLITTER_CONF['keep_headers']
            }
    print(conf)
    return conf


def is_valid_file(file_name):
    '''
    Validate the input file.
    Check if the input file_name exists and if it is a file
    '''
    isValid = os.path.exists(file_name) and os.path.isfile(file_name)
    if isValid is False:
        print("invalid file ", file_name)
    return isValid

if __name__ == '__main__':
    main()
