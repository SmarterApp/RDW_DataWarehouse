import logging
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper,\
    get_all_elements
from smarter_score_batcher.mapping.assessment import get_assessment_mapping
from smarter_score_batcher.mapping.assessment_metadata import get_assessment_metadata_mapping
from smarter_score_batcher.utils.file_utils import csv_file_writer
import os
from smarter_score_batcher.utils.metadata_generator import metadata_generator_bottom_up

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


def get_item_level_data(root):
    '''
    Generate and return item level data as list of lists for given xml root
    '''
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
    csv_data = get_assessment_mapping(root)
    # json_data is a dictionary of the json file format
    json_data = get_assessment_metadata_mapping(root)
    # TODO: write to db in next story


def process_item_level_data(root, csv_file_path):
    matrix_to_feed_csv = get_item_level_data(root)
    return csv_file_writer(csv_file_path, matrix_to_feed_csv)


def generate_csv_from_xml(csv_file_path, xml_file_path):
    '''
    Creates a csv in the given csv file path by reading from the xml file path
    '''
    written = False
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        process_assessment_data(root)
        written = process_item_level_data(root, csv_file_path)
        if written:
            metadata_generator_bottom_up(csv_file_path, generateMetadata=True)
    except ET.ParseError as e:
        '''
        this should not be happened because we already validate against xsd
        '''
        logger.error('csv file[' + csv_file_path + '] is failed to generate: ' + str(e))
        logger.error('this error may be caused because you have an old xsd?')
    except Exception as e:
        if written:
            logger.error('metadata for csv file[' + csv_file_path + '] is failed to updated: ' + str(e))
        else:
            logger.error('csv file[' + csv_file_path + '] is failed to generate: ' + str(e))
            if os.path.exists(csv_file_path):
                os.remove(csv_file_path)
    return written
