from __future__ import absolute_import
import os
import argparse
import time
from celery import chain
from udl2 import W_file_arrived, W_file_expander, W_simple_file_validator, W_file_splitter
from udl2 import message_keys as mk
from udl2_util.udl_mappings import get_json_to_asmt_tbl_mappings
from conf import udl2_conf
from move_to_integration.column_mapping import get_column_mapping

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

    archived_file = os.path.join('/', 'fake', 'path', 'to', 'fake_archived_file.zip')
    batch_id = str(uuid4())

    lzw = WORK_ZONE
    jc_table = {}
    jc = (jc_table, batch_id)

    # TODO: After implementing expander, change generate_message_for_file_arrived() so it includes the actual zipped file.
    arrival_msg = generate_message_for_file_arrived(archived_file, lzw, jc)

    expander_msg = generate_file_expander_msg(lzw, archived_file, jc)
    expander_msg = extend_file_expander_msg_temp(expander_msg, json_file_path, csv_file_path)

    validator_msg = generate_file_validator_msg(lzw, jc)

    splitter_msg = generate_splitter_msg(lzw, jc)

    pipeline_chain = chain(W_file_arrived.task.si(arrival_msg), W_file_expander.task.si(expander_msg),
                           W_simple_file_validator.task.si(validator_msg), W_file_splitter.task.si(splitter_msg))

    result = pipeline_chain.delay()
    # print('RESULT >>>>>>>>>>> ' + str(result.get()))


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


def generate_message_json_to_int(job_control, json_file):
    msg = {
        mk.FILE_TO_LOAD: json_file,
        mk.MAPPINGS: get_json_to_asmt_tbl_mappings(),
        mk.DB_HOST: udl2_conf['postgresql']['db_host'],
        mk.DB_PORT: udl2_conf['postgresql']['db_port'],
        mk.DB_USER: udl2_conf['postgresql']['db_user'],
        mk.DB_NAME: udl2_conf['postgresql']['db_database'],
        mk.DB_PASSWORD: udl2_conf['postgresql']['db_pass'],
        mk.INT_SCHEMA: udl2_conf['udl2_db']['integration_schema'],
        mk.INT_TABLE: 'INT_SBAC_ASMT',  # TODO: acquire this information
        mk.JOB_CONTROL: job_control
    }
    return msg


def generate_msg_report_error(email):
    msg = {
        mk.EMAIL: email
    }
    return msg


def generate_msg_content_validation(job_control):
    msg = {
        mk.JOB_CONTROL: job_control,
        mk.STG_TABLE: 'STG_SBAC_ASMT_OUTCOME'  # TODO: acquire this information
    }
    return msg


def generate_move_to_target(job_control):
    msg = {
        mk.BATCH_ID: job_control[1]
    }
    return msg


def generate_load_to_integration(job_control):
    msg = {
        mk.BATCH_ID: job_control[1],
        mk.INT_TABLE_TYPE: get_column_mapping('staging_to_integration_sbac_asmt_outcome')
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
