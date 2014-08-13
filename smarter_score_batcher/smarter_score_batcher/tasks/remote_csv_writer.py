import logging
from smarter_score_batcher.celery import celery
from smarter_score_batcher.utils.file_utils import csv_file_writer
import os
from smarter_score_batcher.utils.csv_utils import get_item_level_data,\
    process_assessment_data

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


@celery.task(name="tasks.tsb.remote_csv_writer")
def remote_csv_generator(csv_file_path, xml_file_path):
    '''
    Create assessment and item level csv
    '''
    written = False
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        process_assessment_data(root)
        item_level_data = get_item_level_data(root)
        written = csv_file_writer(csv_file_path, item_level_data)
    except ET.ParseError as e:
        logger.error('csv file[' + csv_file_path + '] is failed to generate: ' + str(e))
    except Exception as e:
        logger.error('csv file[' + csv_file_path + '] is failed to generate: ' + str(e))
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
    return written
