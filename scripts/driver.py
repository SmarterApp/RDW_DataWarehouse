from __future__ import absolute_import
from elastic_csv.elastic_csv import generate_stretched_csv_file
import udl2.W_file_splitter
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import shutil
import os
import argparse
import time
import datetime

# Paths to our various directories
THIS_MODULE_PATH = os.path.abspath(__file__)
SRC_DIRECTORY = os.path.dirname(THIS_MODULE_PATH)
ROOT_DIRECTORY = os.path.dirname(SRC_DIRECTORY)
ZONES = os.path.join(ROOT_DIRECTORY, 'zones')
LANDING_ZONE = os.path.join(ZONES, 'landing')
WORK_ZONE = os.path.join(ZONES, 'work')
HISTORY_ZONE = os.path.join(ZONES, 'history_zone')
DATAFILES = os.path.join(ROOT_DIRECTORY, 'datafiles')


def start_pipeline(file_path):
    '''
    Begins the UDL Pipeline process by copying the file found at 'file_path' to the landing zone and
    adding a task to the file_splitter queue

    @param file_path: The file that gets uploaded to the "Landing Zone," beginning the UDL process
    @type file_path: str
    '''

    # Create a unique name for the file when it is placed in the "Landing Zone"
    landing_zone_file_name = create_unique_file_name(file_path)
    landing_zone_file_path = os.path.join(LANDING_ZONE, landing_zone_file_name)
    # Copy the file over, using the new (unique) filename
    shutil.copy(file_path, landing_zone_file_path)
    # Now, add a task to the file splitter queue, passing in the path to the landing zone file
    # and the directory to use when writing the split files
    msg = generate_message_for_file_splitter(landing_zone_file_path)
    udl2.W_file_splitter.task.apply_async([msg], queue='Q_files_to_be_split')


def generate_message_for_file_splitter(landing_zone_file_path):
    msg = {
        'landing_zone_file': landing_zone_file_path,
        'work_zone': WORK_ZONE,
        'history_zone': HISTORY_ZONE,
        # generate batch_id here
        'batch_id': int(datetime.datetime.now().timestamp())
    }
    return msg


def create_unique_file_name(file_path):
    '''
    Given the path to a file, this function takes the file name, x, and appends a timestamp, t, to it, creating the name
    x_t.  This is used to prevent overwriting existing files in the "Landing Zone."

    @param file_path: The file whose name will be used as a template to create a new file name.
    @type file_path: str
    '''

    # This will return the name of the file and the extension in a tuple
    file_name_and_ext = os.path.splitext(os.path.basename(file_path))
    # Get the current time in seconds since the epoch
    time_stamp = int(time.time())
    new_file_name = '%s_%d%s' % (file_name_and_ext[0], time_stamp, file_name_and_ext[1])
    return new_file_name


if __name__ == '__main__':
    '''
    Main function that reads parameters and kicks off the UDL Process
    '''

    parser = argparse.ArgumentParser()
    # These parameters are used only when using the default file (seed.csv) and elastic_csv to dynamically create a csv file
    # They are passed as parameters to generate_stretched_csv_file(...) and a newly created file (output.csv) is created within /datafiles/
    parser.add_argument('-r', dest='row_multiplier', required=False, type=int, default=1, help="number of times to muliply the rows in the seed file.")
    parser.add_argument('-c', dest='column_multiplier', required=False, type=int, default=1, help="number of times to multiply the columns in the seed file.")
    parser.add_argument('-s', dest='source_csv', required=False, default=os.path.join(DATAFILES, 'seed.csv'), help="path to the source file, default is seed.csv")
    parser.add_argument('-o', dest='output_data_csv', required=False, default=os.path.join(DATAFILES, 'test_file.csv'), help="path to the file that will contain the newly generated csv data.")
    parser.add_argument('-m', dest='output_metadata_csv', default=os.path.join(DATAFILES, 'test_file_metadata.csv'), help="path and file name to csv file of metadata for output")
    parser.add_argument('-t', dest='apply_transformation_rules', default='True', help="apply transformation rules or not")
    args = parser.parse_args()

    if args.source_csv == str(os.path.join(DATAFILES, 'seed.csv')):
        conf = {'row_multiplier': args.row_multiplier,
                'column_multiplier': args.column_multiplier,
                'source_csv': args.source_csv,
                'output_data_csv': args.output_data_csv,
                'output_metadata_csv': args.output_metadata_csv,
                'apply_transformation_rules': args.apply_transformation_rules}
        csv_file_path = generate_stretched_csv_file(conf)[0]
    else:
        csv_file_path = args.source_csv

    start_pipeline(csv_file_path)
