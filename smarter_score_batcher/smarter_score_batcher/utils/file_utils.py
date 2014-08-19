'''
Created on Aug 11, 2014

@author: tosako
'''
import os
from edcore.utils.csv_writer import write_csv
from smarter_score_batcher.utils.constants import Constants
import json


def file_writer(path, data, mode=0o700):
    '''
    Creates a file in the specified path and fills with data
    :param path: file to create
    :param data: data to be written
    :param mode: file attribute
    :returns: Truen when file is written
    '''
    # create directory
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(str.encode(data) if type(data) is str else data)
        written = True
    if os.path.exists(path):
        os.chmod(path, mode)
    return written if written else False


def csv_file_writer(csv_file_path, data, header=None, mode=0o700, csv_write_mode='w'):
    '''
    Creates a csv file in the specified path and fills with data
    :param csv_file_path: csv file path
    :param data: data to be written
    :param mode: file attribute
    :returns: True when a file is written
    '''
    # create directory
    written = False
    if data is not None and data:
        os.makedirs(os.path.dirname(csv_file_path), mode=mode, exist_ok=True)
        written = write_csv(csv_file_path, data, header=header, mode=csv_write_mode)
        if os.path.exists(csv_file_path):
            os.chmod(csv_file_path, mode)
    return written


def json_file_writer(file_path, data, mode=0o700):
    '''
    Writes to a JSON file

    :param file_path: the path of the file to write to
    :param dict data: a python dictionary that is the content that is written to the file
    '''
    os.makedirs(os.path.dirname(file_path), mode=mode, exist_ok=True)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def create_path(root_dir, meta, generate_path):
    '''
    Constructs and returns a path from the meta
    :param root_dir: root dir
    :param meta: Meta object
    :param generate_path: function to generate path
    :returns: file path
    '''
    kwargs = {}
    kwargs[Constants.STATE_CODE] = meta.state_code
    kwargs[Constants.ASMT_YEAR] = meta.academic_year
    kwargs[Constants.ASMT_TYPE] = meta.asmt_type
    kwargs[Constants.EFFECTIVE_DATE] = meta.effective_date
    kwargs[Constants.ASMT_SUBJECT] = meta.subject
    kwargs[Constants.ASMT_GRADE] = meta.grade
    kwargs[Constants.DISTRICT_ID] = meta.district_id
    kwargs[Constants.STUDENT_ID] = meta.student_id
    return generate_path(root_dir, **kwargs)
