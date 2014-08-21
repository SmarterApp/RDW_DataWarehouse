from smarter_score_batcher.mapping.assessment import get_assessment_mapping
from smarter_score_batcher.mapping.assessment_metadata import get_assessment_metadata_mapping
from smarter_score_batcher.utils.file_utils import csv_file_writer, \
    json_file_writer, make_dirs
from smarter_score_batcher.utils.item_level_utils import get_item_level_data
import os
from smarter_score_batcher.utils.metadata_generator import metadata_generator_bottom_up
from smarter_score_batcher.utils.file_lock import FileLock
import logging
import fcntl
import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


def process_assessment_data(root, meta, base_dir):
    '''
    process assessment data
    :param root: xml root document
    '''
    # Create dir name based on state code and file name from asmt id
    directory = os.path.join(base_dir, meta.state_code, meta.asmt_id)
    make_dirs(directory)
    generate_assessment_metadata_file(root, os.path.join(directory, meta.asmt_id + '.json'))
    generate_assessment_file(root, os.path.join(directory, meta.asmt_id + '.csv'))


def generate_assessment_file(root, file_path):
    '''
    Append to existing assessment file if it exists
    Else write header and content into the file
    '''
    def lock_and_write(data):
        with FileLock(file_path, mode='a', lock_operation=fcntl.LOCK_EX | fcntl.LOCK_NB) as fl:
            header = data.header if fl.new_file is True else None
            csv_file_writer(file_path, [data.values], header=header, csv_write_mode='a')
    data = get_assessment_mapping(root)
    while True:
        try:
            lock_and_write(data)
            break
        except IOError:
            # spin lock
            time.sleep(1)
        except:
            raise

  
def generate_assessment_metadata_file(root, file_path):
    '''
    Only write to JSON metadata file if the file doesn't already exist
    '''
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            data = get_assessment_metadata_mapping(root)
            json_file_writer(f, data)


def process_item_level_data(root, meta, csv_file_path):
    '''
    Get Item level data and writes it to csv files
    '''
    data = get_item_level_data(root, meta)
    return csv_file_writer(csv_file_path, data)


def generate_csv_from_xml(meta, csv_file_path, xml_file_path, work_dir):
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
        process_assessment_data(root, meta, work_dir)
        written = process_item_level_data(root, meta, csv_file_path)
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
