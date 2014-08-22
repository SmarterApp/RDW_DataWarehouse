'''
Created on Aug 11, 2014

@author: tosako
'''
import os
from edcore.utils.csv_writer import write_csv
from smarter_score_batcher.utils.constants import Constants
import json


def make_dirs(path, mode=0o700, exist_ok=True):
    '''
    Create the directory for a path given
    '''
    os.makedirs(path, mode=mode, exist_ok=exist_ok)


def file_writer(path, data, mode=0o700):
    '''
    Creates a file in the specified path and fills with data
    :param path: file to create
    :param data: data to be written
    :param mode: file attribute
    :returns: Truen when file is written
    '''
    # create directory
    make_dirs(os.path.dirname(path))
    with open(path, 'wb') as f:
        f.write(str.encode(data) if type(data) is str else data)
        written = True
    if os.path.exists(path):
        os.chmod(path, mode)
    return written if written else False


def csv_file_writer(file_object, data, header=None):
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
        written = write_csv(file_object, data, header=header)
    return written


def json_file_writer(file_descriptor, data):
    '''
    Writes to a JSON file

    :param file_descriptor: the file descriptor for the file
    :param dict data: a python dictionary that is the content that is written to the file
    '''
    json.dump(data, file_descriptor, indent=4)


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
