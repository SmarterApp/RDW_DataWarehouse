from smarter_score_batcher.mapping.assessment import get_assessment_mapping
from smarter_score_batcher.mapping.assessment_metadata import get_assessment_metadata_mapping
from smarter_score_batcher.utils.file_utils import csv_file_writer,\
    json_file_writer
from smarter_score_batcher.utils.item_level_utils import get_item_level_data
import os
from smarter_score_batcher.utils.metadata_generator import metadata_generator_bottom_up
from smarter_score_batcher.utils.file_lock import FileLock
import logging
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


def process_assessment_data(root):
    '''
    process assessment data
    :param root: xml root document
    '''
    # csv_data is an AssessmentData object
    csv_data = get_assessment_mapping(root)
    json_data = get_assessment_metadata_mapping(root)

    json_file_path = '/tmp/blah/somepath.json'
    csv_file_path = '/tmp/blah/somepath.csv'
    os.makedirs(os.path.dirname(json_file_path), mode=0o700, exist_ok=True)
    
    generate_assessment_file(csv_file_path, csv_data)
    generate_assessment_metadata_file(json_file_path, json_data)


def generate_assessment_file(file_path, data):
    '''
    Append to existing assessment file if it exists
    Else write header and content into the file
    '''
    with FileLock(file_path) as fl:
        header = data.header if fl.created_file is True else None
        csv_file_writer(file_path, [data.values], header=header, csv_write_mode='a')
        

def generate_assessment_metadata_file(file_path, data):
    '''
    Only write to JSON metadata file if the file doesn't already exist
    '''
    if not os.path.exists(file_path):
        with FileLock(file_path):
            json_file_writer(file_path, data)


def process_item_level_data(root, csv_file_path):
    '''
    Get Item level data and writes it to csv files
    '''
    data = get_item_level_data(root)
    return csv_file_writer(csv_file_path, data)


def generate_csv_from_xml(csv_file_path, xml_file_path):
    '''
    Creates a csv in the given csv file path by reading from the xml file path
    :param csv_file_path: csv file path
    :param xml_file_path: xml file path
    :returns: True when csv file is generated
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
