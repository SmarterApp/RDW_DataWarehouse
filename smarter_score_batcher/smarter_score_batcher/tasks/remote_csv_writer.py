import logging
from smarter_score_batcher.celery import celery
from smarter_score_batcher.utils.file_utils import csv_file_writer
from smarter_score_batcher.utils.csv_utils import get_all_elements_for_tsb_csv

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


@celery.task(name="tasks.tsb.remote_csv_writer")
def remote_csv_generator(csv_file_path, xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        logger.error(str(e))
    matrix_to_feed_csv = get_all_elements_for_tsb_csv(root, './Opportunity/Item')
    return csv_file_writer(csv_file_path, matrix_to_feed_csv)
