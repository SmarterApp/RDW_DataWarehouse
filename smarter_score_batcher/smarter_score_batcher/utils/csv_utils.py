from smarter_score_batcher.mapping.assessment import get_assessment_mapping
from smarter_score_batcher.mapping.assessment_metadata import get_assessment_metadata_mapping
from smarter_score_batcher.utils.file_utils import csv_file_writer, \
    json_file_writer, make_dirs
from smarter_score_batcher.utils.item_level_utils import get_item_level_data
import os
from smarter_score_batcher.utils.metadata_generator import metadata_generator_bottom_up
from smarter_score_batcher.utils.file_lock import FileLock
import logging
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
    lock_and_write(root, os.path.join(directory, meta.asmt_id))


def lock_and_write(root, file_path, mode=0o700):
    '''
    Append to existing assessment file if it exists
    Else write header and content into the file
    '''
    csv_file_path = file_path + '.csv'
    json_file_path = file_path + '.json'
    parent = os.path.dirname(file_path)
    make_dirs(parent, mode=mode, exist_ok=True)
    SPIN_LOCK = True
    while SPIN_LOCK:
        try:
            with FileLock(csv_file_path, mode='a', no_block_lock=True) as fl:
                SPIN_LOCK = False
                generate_assessment_file(fl.file_object, root, header=fl.new_file)
                if not os.path.isfile(json_file_path):
                    generate_assessment_metadata_file(root, json_file_path)
        except BlockingIOError:
            # spin lock
            time.sleep(1)
        except Exception as e:
            raise


def generate_assessment_file(file_object, root, header=False):
    '''
    lock file then write
    non-block lock, if the file is already locked, then raise IOError instead of waiting.
    :param file_path: file path
    :param data: data
    '''
    data = get_assessment_mapping(root)
    csv_file_writer(file_object, [data.values], header=data.header if header else None)


def generate_assessment_metadata_file(root, file_path):
    '''
    Only write to JSON metadata file if the file doesn't already exist
    '''
    try:
        # create file only when file does not eixst
        with open(file_path, 'x') as f:
            data = get_assessment_metadata_mapping(root)
            json_file_writer(f, data)
    except:
        # most likely file already exist
        pass


def process_item_level_data(root, meta, csv_file_path):
    '''
    Get Item level data and writes it to csv files
    '''
    written = False
    data = get_item_level_data(root, meta)
    dirname = os.path.dirname(csv_file_path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname, exist_ok=True)
    with open(csv_file_path, 'w') as f:
        written = csv_file_writer(f, data)
    return written


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
        # this should not be happened because we already validate against xsd
        logger.error(str(e))
        logger.error('this error may be caused because you have an old xsd?')
    except Exception as e:
        logger.error(str(e))
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
    return written
