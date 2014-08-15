from smarter_score_batcher.celery import celery
from smarter_score_batcher.utils.csv_utils import generate_csv_from_xml


@celery.task(name="tasks.tsb.remote_csv_writer")
def remote_csv_generator(csv_file_path, xml_file_path):
    '''
    celery task to generate csv from given xml path
    :param csv_file_path: csv file path
    :param xml_file_path: xml file path
    :returns: True when file is written
    '''
    return generate_csv_from_xml(csv_file_path, xml_file_path)
