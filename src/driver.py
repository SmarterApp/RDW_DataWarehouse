from __future__ import absolute_import
from elastic_csv.elastic_csv import generate_stretched_csv_file
import udl2.W_file_splitter
import shutil
import os
import argparse
import datetime
import time


THIS_MODULE_PATH = os.path.abspath(__file__)
SRC_DIRECTORY = os.path.dirname(THIS_MODULE_PATH)
ROOT_DIRECTORY = os.path.dirname(SRC_DIRECTORY)
ZONES = os.path.join(ROOT_DIRECTORY, 'zones')
LANDING_ZONE = os.path.join(ZONES, 'landing')
WORK_ZONE = os.path.join(ZONES, 'work')
DATAFILES = os.path.join(ROOT_DIRECTORY, 'datafiles')


def start_pipeline(file_path):
    landing_zone_file_name = create_unique_file_name(file_path)
    landing_zone_file_path = os.path.join(LANDING_ZONE, landing_zone_file_name)
    shutil.copy(file_path, landing_zone_file_path)
    udl2.W_file_splitter.task.apply_async([{'input_file':landing_zone_file_path, 'output_path': WORK_ZONE}], queue='Q_files_to_be_split')
    
    
def create_unique_file_name(file_path):
    file_name_and_ext = os.path.splitext(os.path.basename(file_path))
    current_datetime = datetime.datetime.now()
    time_stamp = int(time.mktime(current_datetime.timetuple()))
    new_file_name = '%s_%d%s' % (file_name_and_ext[0], time_stamp, file_name_and_ext[1])
    return new_file_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest='row_multiplier', required=False, type=int, default=1, help="number of times to muliply the rows in the seed file.")
    parser.add_argument('-c', dest='column_multiplier', required=False, type=int, default=1, help="number of times to multiply the columns in the seed file.")
    parser.add_argument('-s', dest='source_csv', required=False, default=os.path.join(DATAFILES, 'seed.csv'), help="path to the source file, default is seed.csv")
    parser.add_argument('-o', dest='output_data_csv', required=False, default=os.path.join(DATAFILES, 'output.csv'), help="path to the file that will contain the newly generated csv data.")
    args = parser.parse_args()

    if args.source_csv == str(os.path.join(DATAFILES, 'seed.csv')):
        conf = {'row_multiplier': args.row_multiplier,
                'column_multiplier': args.column_multiplier,
                'source_csv': args.source_csv,
                'output_data_csv': args.output_data_csv}
        csv_file_path = generate_stretched_csv_file(conf)
    else:
        csv_file_path = args.source_csv

    start_pipeline(csv_file_path)
