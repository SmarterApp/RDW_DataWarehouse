from smarter_score_batcher.celery import celery
from smarter_score_batcher.utils.csv_utils import generate_csv_from_xml


@celery.task(name="tasks.tsb.remote_csv_writer")
def remote_csv_generator(csv_file_path, xml_file_path):
    return generate_csv_from_xml(csv_file_path, xml_file_path)
