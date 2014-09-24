from smarter_score_batcher.celery import celery
from smarter_score_batcher.processing.file_processor import generate_csv_from_xml,\
    prepare_assessment_dir
from smarter_score_batcher.error.exceptions import TSBException
from smarter_score_batcher.error.error_handler import handle_error
import os
from smarter_score_batcher.constant import Extensions


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
        mode=0o700
        rtn = generate_csv_from_xml(meta, csv_file_path, xml_file_path, work_dir, mode=mode)
    except TSBException as e:
        # all TSB exception should be caught in here
        state_code = meta.state_code
        asmt_id = meta.asmt_id
        directory = prepare_assessment_dir(work_dir, state_code, asmt_id, mode=0o700)
        err_file_path = os.path.join(directory, asmt_id+Extensions.ERR)
        handle_error(e, err_file_path)
    return rtn
