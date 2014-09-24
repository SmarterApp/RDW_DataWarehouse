from smarter_score_batcher.celery import celery
from smarter_score_batcher.processing.file_processor import generate_csv_from_xml
from smarter_score_batcher.error.exceptions import TSBException
from smarter_score_batcher.error.error_handler import handle_error


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
        rtn = generate_csv_from_xml(meta, csv_file_path, xml_file_path, work_dir)
    except TSBException as e:
        handle_error(e)
    return rtn
