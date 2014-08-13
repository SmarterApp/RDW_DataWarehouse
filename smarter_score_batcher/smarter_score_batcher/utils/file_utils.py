'''
Created on Aug 11, 2014

@author: tosako
'''
import os
from edcore.utils.csv_writer import write_csv
from smarter_score_batcher.utils.constants import Constants


def file_writer(path, data, mode=0o700):
    '''
    Creates a file in the specified path and fills with data
    '''
    # create directory
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(str.encode(data) if type(data) is str else data)
        written = True
    if os.path.exists(path):
        os.chmod(path, mode)
    return written if written else False


def csv_file_writer(csv_file_path, data, mode=0o700):
    '''
    Creates a csv file in the specified path and fills with data
    '''
    # create directory
    written = False
    if data is not None and data:
        os.makedirs(os.path.dirname(csv_file_path), mode=mode, exist_ok=True)
        written = write_csv(csv_file_path, data, header=None)
        if os.path.exists(csv_file_path):
            os.chmod(csv_file_path, mode)
    return written if written else False


def create_path(root_dir, meta, generate_path):
    '''
    Constructs and returns a path from the meta
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
