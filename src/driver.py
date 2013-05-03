from __future__ import absolute_import
import udl2.W_file_splitter
import shutil
import os
import argparse
import datetime
import time


THIS_MODULE_PATH = os.path.abspath(__file__)
SRC_DIRECTORY = os.path.dirname(THIS_MODULE_PATH)
ROOT_DIRECTORY = os.path.dirname(SRC_DIRECTORY)
LANDING_ZONE = os.path.join(ROOT_DIRECTORY, 'landing_zone')



def main(file_path):
    landing_zone_file_name = create_unique_file_name(file_path)
    landing_zone_file_path = os.path.join(LANDING_ZONE, landing_zone_file_name)
    shutil.copy(file_path, landing_zone_file_path)
    udl2.W_file_splitter.task.apply_async([landing_zone_file_path], queue='Q_files_to_be_split')
    
    
def create_unique_file_name(file_path):
    file_name_and_ext = os.path.splitext(os.path.basename(file_path))
    current_datetime = datetime.datetime.now()
    time_stamp = int(time.mktime(current_datetime.timetuple()))
    new_file_name = '%s_%d%s' % (file_name_and_ext[0], time_stamp, file_name_and_ext[1])
    return new_file_name


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--file', help='The path to the file to put in the landing-zone.', required=False)
    args = argument_parser.parse_args()
    file_path = args.file
    if not file_path:
        default_file_path = os.path.join(ROOT_DIRECTORY, 'datafiles', 'dim_staff.csv')
        file_path = default_file_path
    main(file_path)
