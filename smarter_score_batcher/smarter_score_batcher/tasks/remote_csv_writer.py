from smarter_score_batcher.celery import celery
from smarter_score_batcher.processing.file_processor import generate_csv_from_xml, \
    prepare_assessment_dir
from smarter_score_batcher.error.exceptions import TSBException,\
    TSBSecurityException
from smarter_score_batcher.error.error_handler import handle_error
import os
from smarter_score_batcher.constant import Extensions
from smarter_score_batcher.error.error_codes import ErrorCode, ErrorSource


@celery.task(name="tasks.tsb.remote_csv_writer")
def remote_csv_generator(meta, csv_file_path, xml_file_path, work_dir):
    '''
    celery task to generate csv from given xml path
    :param csv_file_path: csv file path
    :param xml_file_path: xml file path
    :returns: True when file is written
    '''
    rtn = False
    try:
        mode = 0o700
        rtn = generate_csv_from_xml(meta, csv_file_path, xml_file_path, work_dir, mode=mode)
    except TSBException as e:
        # all TSB exception should be caught in here
        e.err_input = 'student_guid: ' + meta.student_id
        state_code = meta.state_code
        asmt_id = meta.asmt_id
        directory = prepare_assessment_dir(work_dir, state_code, asmt_id, mode=0o700)
        err_file_path = os.path.abspath(os.path.join(directory, asmt_id + Extensions.ERR))
        json_file_path = os.path.abspath(os.path.join(directory, asmt_id + Extensions.JSON))
        if os.path.commonprefix(directory, err_file_path, json_file_path) != directory:
            raise TSBSecurityException(msg='Creating file path error requested dir[' + err_file_path + '] and [' + json_file_path + ']', err_code=ErrorCode.PATH_TRAVERSAL_DETECTED, err_source=ErrorSource.REMOTE_CSV_GENERATOR)
        handle_error(e, err_file_path, xml_file_path, json_file_path)
    return rtn
