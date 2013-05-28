from __future__ import absolute_import
import os
import argparse
import time
from celery import chain
from udl2 import W_file_arrived, W_file_expander, W_simple_file_validator, W_file_splitter
from udl2 import message_keys as mk

# Paths to our various directories
THIS_MODULE_PATH = os.path.abspath(__file__)
SRC_DIRECTORY = os.path.dirname(THIS_MODULE_PATH)
ROOT_DIRECTORY = os.path.dirname(SRC_DIRECTORY)
ZONES = os.path.join(ROOT_DIRECTORY, 'zones')
LANDING_ZONE = os.path.join(ZONES, 'landing')
ARRIVALS = os.path.join(ZONES, 'arrivals')
WORK_ZONE = os.path.join(LANDING_ZONE, 'work')
HISTORY_ZONE = os.path.join(LANDING_ZONE, 'history')
DATAFILES = os.path.join(ROOT_DIRECTORY, 'datafiles')

# Keys for validator message
FILE_TO_VALIDATE_NAME = 'file_to_validate_name'
FILE_TO_VALIDATE_DIR = 'file_to_validate_dir'
BATCH_ID = 'batch_id'

def start_pipeline(csv_file_path, json_file_path):
    '''
    Begins the UDL Pipeline process by copying the file found at 'csv_file_path' to the landing zone arrivals dir and
    initiating our main pipeline chain.

    @param csv_file_path: The file that gets uploaded to the "Landing Zone" Arrival dir beginning the UDL process
    @type csv_file_path: str
    '''

    # Create a unique name for the file when it is placed in the "Landing Zone"
    # arrivals_dir = ARRIVALS
    # unique_filename = create_unique_file_name(csv_file_path)
    # full_path_to_arrival_dir_file = os.path.join(arrivals_dir, unique_filename)
    # Copy the file over, using the new (unique) filename
    # shutil.copy(csv_file_path, full_path_to_arrival_dir_file)
    # Now, add a task to the file splitter queue, passing in the path to the landing zone file
    # and the directory to use when writing the split files

    archived_file = os.path.join('fake', 'path', 'to', 'fake_archived_file.zip')
    jc_table_conf = {}
    lzw = WORK_ZONE

    # TODO: After implementing expander, change generate_message_for_file_arrived() so it includes the actual zipped file.
    arrival_msg = generate_message_for_file_arrived(archived_file, lzw, jc_table_conf)
    arrival_msg = extend_arrival_msg_temp(arrival_msg, csv_file_path, json_file_path)

    pipeline_chain = chain(W_file_arrived.task.s(arrival_msg), W_file_expander.task.s(), W_simple_file_validator.task.s(),
                           W_file_splitter.task.s())
    result = pipeline_chain.delay()


def generate_message_for_file_arrived(archived_file_path, lzw, jc_table_conf):
    msg = {
        mk.INPUT_FILE_PATH: archived_file_path,
        mk.LANDING_ZONE_WORK_DIR: lzw,
        mk.JOB_CONTROL_TABLE_CONF: jc_table_conf
    }
    return msg


def extend_arrival_msg_temp(msg, csv_file_path, json_file_path):
    msg.update({mk.CSV_FILENAME: csv_file_path})
    msg.update({mk.JSON_FILENAME: json_file_path})
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
