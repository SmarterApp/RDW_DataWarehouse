from udl2.W_file_splitter import task
import argparse
import os


def main():
    # get parameters from command lines
    parm = get_parameters()

    # verify input parameters
    try:
        if int(parm['parts']) < 0:
            print("The value for parts should be a positive integer")
            exit()
        if int(parm['number_of_rows']) < 0:
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


def get_parameters():
    parser = argparse.ArgumentParser(description='File Splitter Worker')
    parser.add_argument("-p", "--parts", type=int, default=0, help="number of parts to be splitted")
    parser.add_argument("-n", "--number_of_rows", type=int, default=100, help="number of rows in each sub file")
    parser.add_argument("-i", "--input_file", required=True, help="input file")
    parser.add_argument("-o", "--output_path", required=True, help="output directory")
    args = parser.parse_args()
    conf = {
            'parts': args.parts,
            'number_of_rows': args.number_of_rows,
            'input_file': args.input_file,
            'output_path': args.output_path
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
