from __future__ import absolute_import
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

# Keys for validator message
FILE_TO_VALIDATE_NAME = 'file_to_validate_name'
FILE_TO_VALIDATE_DIR = 'file_to_validate_dir'
BATCH_ID = 'batch_id'

def start_pipeline(csv_file_path, json_file_path):
    '''
    Begins the UDL Pipeline process by copying the file found at 'file_path' to the landing zone and
    initiating our main pipeline chain.

    @param csv_file_path: The file that gets uploaded to the "Landing Zone," beginning the UDL process
    @type csv_file_path: str
    '''

    # Create a unique name for the file when it is placed in the "Landing Zone"
    landing_zone_file_dir = LANDING_ZONE
    landing_zone_file_name = create_unique_file_name(csv_file_path)
    full_path_to_landing_zone_file = os.path.join(landing_zone_file_dir, landing_zone_file_name)
    # Copy the file over, using the new (unique) filename
    shutil.copy(csv_file_path, full_path_to_landing_zone_file)
    # Now, add a task to the file splitter queue, passing in the path to the landing zone file
    # and the directory to use when writing the split files
    validator_msg = generate_message_for_file_validator(landing_zone_file_dir, landing_zone_file_name)

    # TODO: Kick off the pipeline using the validator message as a starting point
    #udl2.W_file_splitter.task.apply_async([validator_msg], queue='Q_files_received')


def generate_message_for_file_validator(landing_zone_file_dir, landing_zone_file_name):
    msg = {
        FILE_TO_VALIDATE_DIR:landing_zone_file_dir,
        FILE_TO_VALIDATE_NAME: landing_zone_file_name,
        BATCH_ID: int(datetime.datetime.now().timestamp())
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
    parser.add_argument('-c', dest='source_csv', required=True, help="path to the source csv file.")
    parser.add_argument('-j', dest='source_json', required=True, help="path to the source json file.")
    parser.add_argument('-t', dest='apply_transformation_rules', default='True', help="apply transformation rules or not")
    args = parser.parse_args()

    start_pipeline(args.source_csv, args.source_json)
