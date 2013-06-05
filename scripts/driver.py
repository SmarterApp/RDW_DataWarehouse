from __future__ import absolute_import
import os
import argparse
import time
from celery import chain
from udl2 import W_file_arrived, W_file_expander, W_simple_file_validator, W_file_splitter, W_file_content_validator, \
    W_load_json_to_integration, W_load_to_integration_table, W_load_from_integration_to_star
from udl2 import message_keys as mk
from uuid import uuid4
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp


# Paths to our various directories
#THIS_MODULE_PATH = os.path.abspath(__file__)
#SRC_DIRECTORY = os.path.dirname(THIS_MODULE_PATH)
#ROOT_DIRECTORY = os.path.dirname(SRC_DIRECTORY)
#ZONES = os.path.join(ROOT_DIRECTORY, 'zones')
#LANDING_ZONE = os.path.join(ZONES, 'landing')
#ARRIVALS = os.path.join(ZONES, 'arrivals')
#WORK_ZONE = os.path.join(LANDING_ZONE, 'work')
#HISTORY_ZONE = os.path.join(LANDING_ZONE, 'history')
#DATAFILES = os.path.join(ROOT_DIRECTORY, 'datafiles')


def start_pipeline(csv_file_path, json_file_path, udl2_conf):
    '''
    Begins the UDL Pipeline process by copying the file found at 'csv_file_path' to the landing zone arrivals dir and
    initiating our main pipeline chain.

    @param csv_file_path: The csv file that gets uploaded to the "Landing Zone" Arrival dir beginning the UDL process
    @type csv_file_path: str
    @param json_file_path: The json file that gets uploaded to the "Landing Zone" Arrival dir beginning the UDL process
    @type json_file_path: str
    @param udl2_conf: udl2 system configuration dictionary
    @type udl2: dict
    '''

    # Create a unique name for the file when it is placed in the "Landing Zone"
    # arrivals_dir = ARRIVALS
    # unique_filename = create_unique_file_name(csv_file_path)
    # full_path_to_arrival_dir_file = os.path.join(arrivals_dir, unique_filename)
    # Copy the file over, using the new (unique) filename
    # shutil.copy(csv_file_path, full_path_to_arrival_dir_file)
    # Now, add a task to the file splitter queue, passing in the path to the landing zone file
    # and the directory to use when writing the split files

    # Prepare parameters for task msgs
    archived_file = os.path.join('/', 'fake', 'path', 'to', 'fake_archived_file.zip')
    batch_id = str(uuid4())
    lzw = udl2_conf['zones']['work']
    jc_table = {}
    jc = (jc_table, batch_id)

    # TODO: After implementing expander, change generate_message_for_file_arrived() so it includes the actual zipped file.
    arrival_msg = generate_message_for_file_arrived(archived_file, lzw, jc)

    expander_msg = generate_file_expander_msg(lzw, archived_file, jc)
    expander_msg = extend_file_expander_msg_temp(expander_msg, json_file_path, csv_file_path)

    simple_file_validator_msg = generate_file_validator_msg(lzw, jc)
    splitter_msg = generate_splitter_msg(lzw, jc)
    file_content_validator_msg = generate_file_content_validator_msg()
    load_json_msg = generate_load_json_msg(lzw, jc)
    load_to_int_msg = generate_load_to_int_msg(jc)
    integration_to_star_msg = generate_integration_to_star_msg(batch_id)

    pipeline_chain_1 = chain(W_file_arrived.task.si(arrival_msg), W_file_expander.task.si(expander_msg),
                           W_simple_file_validator.task.si(simple_file_validator_msg), W_file_splitter.task.si(splitter_msg),
                           W_file_content_validator.task.si(file_content_validator_msg), W_load_json_to_integration.task.si(load_json_msg),
                           W_load_to_integration_table.task.si(load_to_int_msg),
                           W_load_from_integration_to_star.explode_to_dims.si(integration_to_star_msg),
                           W_load_from_integration_to_star.explode_to_fact.si(integration_to_star_msg))

    result = pipeline_chain_1.delay()


def generate_message_for_file_arrived(archived_file_path, lzw, jc):
    msg = {
        mk.INPUT_FILE_PATH: archived_file_path,
        mk.LANDING_ZONE_WORK_DIR: lzw,
        mk.JOB_CONTROL: jc
    }
    return msg


def generate_file_expander_msg(landing_zone_work_dir, file_to_expand, jc):
    msg = {
        mk.LANDING_ZONE_WORK_DIR: landing_zone_work_dir,
        mk.FILE_TO_EXPAND: file_to_expand,
        # Tuple containing config info for job control table and the batch_id for the file upload
        mk.JOB_CONTROL: jc
    }
    return msg


def extend_file_expander_msg_temp(msg, json_filename, csv_filename):
    msg[mk.JSON_FILENAME] = json_filename
    msg[mk.CSV_FILENAME] = csv_filename
    return msg


def generate_file_validator_msg(landing_zone_work_dir, job_control):
    msg = {
        mk.LANDING_ZONE_WORK_DIR: landing_zone_work_dir,
        mk.JOB_CONTROL: job_control
    }
    return msg


def generate_splitter_msg(lzw, jc):
    splitter_msg = {
        mk.LANDING_ZONE_WORK_DIR: lzw,
        mk.JOB_CONTROL: jc,
        # TODO: remove hard-coded 4
        mk.PARTS: 4
    }
    return splitter_msg

def generate_file_content_validator_msg():
    # TODO: Implement me please, empty maps are boring.
    return {}

def generate_load_json_msg(lzw, jc):
    msg = {
        mk.LANDING_ZONE_WORK_DIR: lzw,
        mk.JOB_CONTROL: jc
    }
    return msg

def generate_load_to_int_msg(jc):
    msg = {
        mk.JOB_CONTROL: jc
    }
    return msg


def generate_msg_report_error(email):
    msg = {
        mk.EMAIL: email
    }
    return msg


def generate_move_to_target(job_control):
    msg = {
        mk.BATCH_ID: job_control[1]
    }
    return msg

def generate_integration_to_star_msg(batch_id):
    msg = {
        mk.BATCH_ID: batch_id
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
    parser.add_argument('-f', dest='config_file', default=UDL2_DEFAULT_CONFIG_PATH_FILE, help="configuration file for UDL2")
    args = parser.parse_args()

    if args.config_file is None:
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    else:
        config_path_file = args.config_file
    udl2_conf = imp.load_source('udl2_conf', config_path_file)
    from udl2_conf import udl2_conf
    start_pipeline(args.source_csv, args.source_json, udl2_conf)
