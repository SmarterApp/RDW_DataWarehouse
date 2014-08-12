'''
Created on Aug 11, 2014

@author: tosako
'''
import os
from edcore.utils.csv_writer import write_csv


def file_writer(path, data, mode=0o700):
    # create directory
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(str.encode(data) if type(data) is str else data)
        written = True
    if os.path.exists(path):
        os.chmod(path, mode)
    return written if written else False


def csv_file_writer(csv_file_path, data, mode=0o700):
    # create directory
    os.makedirs(os.path.dirname(csv_file_path), mode=mode, exist_ok=True)
    written = write_csv(csv_file_path, data, header=None)
    if os.path.exists(csv_file_path):
        os.chmod(csv_file_path, mode)
    return written if written else False


def create_path(root_dir, meta, generate_path):
    kwargs = {}
    kwargs['state_code'] = meta.state_code
    kwargs['asmt_year'] = meta.academic_year
    kwargs['asmt_type'] = meta.asmt_type
    kwargs['effective_date'] = meta.effective_date
    kwargs['asmt_subject'] = meta.subject
    kwargs['asmt_grade'] = meta.grade
    kwargs['district_id'] = meta.district_id
    kwargs['student_id'] = meta.student_id
    return generate_path(root_dir, **kwargs)
