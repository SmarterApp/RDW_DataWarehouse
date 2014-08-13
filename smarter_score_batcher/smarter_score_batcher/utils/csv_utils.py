import logging
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper,\
    get_all_elements
from smarter_score_batcher.mapping.csv_metadata import get_csv_mapping
from smarter_score_batcher.mapping.json_metadata import get_json_mapping
from smarter_score_batcher.utils.file_utils import csv_file_writer
import os
from smarter_score_batcher.utils.metadata_generator import metadata_generator_bottom_up

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


def get_item_level_data(root):
    student_guid = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='StudentIdentifier']", "value", "context")
    matrix = []
    list_of_elements = get_all_elements(root, './Opportunity/Item')
    for element_item in list_of_elements:
        key = element_item.get('key')
        segmentId = element_item.get('segmentId')
        position = element_item.get('position')
        clientId = element_item.get('clientId')
        operational = element_item.get('operational')
        isSelected = element_item.get('isSelected')
        format_type = element_item.get('format')
        score = element_item.get('score')
        scoreStatus = element_item.get('scoreStatus')
        adminDate = element_item.get('adminDate')
        numberVisits = element_item.get('numberVisits')
        strand = element_item.get('strand')
        contentLevel = element_item.get('contentLevel')
        pageNumber = element_item.get('pageNumber')
        pageVisits = element_item.get('pageVisits')
        pageTime = element_item.get('pageTime')
        dropped = element_item.get('dropped')
        row = [key, student_guid, segmentId, position, clientId, operational, isSelected, format_type, score, scoreStatus, adminDate, numberVisits, strand, contentLevel, pageNumber, pageVisits, pageTime, dropped]
        matrix.append(row)
    return matrix


def process_assessment_data(root):
    # csv_data is a dictionary that can be inserted into db
    csv_data = get_csv_mapping(root)
    # json_data is a dictionary of the json file format
    json_data = get_json_mapping(root)
    # TODO: write to db in next story


def generate_csv_from_xml(csv_file_path, xml_file_path):
    written = False
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        process_assessment_data(root)
        matrix_to_feed_csv = get_item_level_data(root)
        written = csv_file_writer(csv_file_path, matrix_to_feed_csv)
        if written:
            metadata_generator_bottom_up(csv_file_path, generateMetadata=True)
    except ET.ParseError as e:
        logger.error('csv file[' + csv_file_path + '] is failed to generate: ' + str(e))
    except Exception as e:
        if written:
            logger.error('metadata for csv file[' + csv_file_path + '] is failed to updated: ' + str(e))
        else:
            logger.error('csv file[' + csv_file_path + '] is failed to generate: ' + str(e))
            if os.path.exists(csv_file_path):
                os.remove(csv_file_path)
    return written
