'''
Created on Aug 28, 2014

@author: tosako
'''
import os
import logging
import time
from smarter_score_batcher.utils.file_lock import FileLock
from smarter_score_batcher.processing.assessment import get_assessment_mapping
from smarter_score_batcher.processing.assessment_metadata import get_assessment_metadata_mapping
from smarter_score_batcher.utils.item_level_utils import get_item_level_data
from smarter_score_batcher.utils.file_utils import csv_file_writer, \
    json_file_writer
from smarter_score_batcher.utils.metadata_generator import metadata_generator_bottom_up
from smarter_score_batcher.error.exceptions import GenerateCSVException, \
    TSBException
from smarter_score_batcher.error.error_codes import ErrorSource, ErrorCode

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


logger = logging.getLogger("smarter_score_batcher")


def process_assessment_data(root, meta, base_dir, mode=0o700):
    '''
    process assessment data
    :param root: xml root document
    '''
    # Create dir name based on state code and file name from asmt id
    directory = prepare_assessment_dir(base_dir, meta.state_code, meta.asmt_id, mode=mode)
    lock_and_write(root, os.path.join(directory, meta.asmt_id), mode=mode)


def generate_assessment_file(file_object, root, metadata_file_path, header=False):
    '''
    lock file then write
    non-block lock, if the file is already locked, then raise IOError instead of waiting.
    :param file_path: file path
    :param data: data
    '''
    data = get_assessment_mapping(root, metadata_file_path)
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
    except Exception as e:
        # most likely file already exist
        raise


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


def lock_and_write(root, file_path, mode=0o700):
    '''
    Append to existing assessment file if it exists
    Else write header and content into the file
    '''
    csv_file_path = file_path + '.csv'
    json_file_path = file_path + '.json'
    parent = os.path.dirname(file_path)
    os.makedirs(parent, mode=mode, exist_ok=True)
    SPIN_LOCK = True
    while SPIN_LOCK:
        try:
            with FileLock(csv_file_path, mode='a', no_block_lock=True) as fl:
                SPIN_LOCK = False
                if not os.path.isfile(json_file_path):
                    generate_assessment_metadata_file(root, json_file_path)
                generate_assessment_file(fl.file_object, root, json_file_path, header=fl.new_file)
        except BlockingIOError:
            # spin lock
            time.sleep(1)
        except TSBException:
            raise
        except Exception as e:
            raise TSBException(str(e), err_source=ErrorSource.LOCK_AND_WRITE)


def generate_csv_from_xml(meta, csv_file_path, xml_file_path, work_dir, mode=0o700):
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
        process_assessment_data(root, meta, work_dir, mode=mode)
        written = process_item_level_data(root, meta, csv_file_path)
        if written:
            metadata_generator_bottom_up(csv_file_path, generateMetadata=True)
    except ET.ParseError as e:
        # this should not be happened because we already validate against xsd
        error_msg = str(e)
        logger.error(error_msg)
        logger.error('this error may be caused because you have an old xsd?')
        raise GenerateCSVException(error_msg, err_code=ErrorCode.CSV_PARSE_ERROR, err_source=ErrorSource.GENERATE_CSV_FROM_XML)
    except TSBException as e:
        error_msg = str(e)
        logger.error(error_msg)
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(error_msg)
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        raise GenerateCSVException(error_msg, err_code=ErrorCode.CSV_GENERATE_ERROR, err_source=ErrorSource.GENERATE_CSV_FROM_XML)

    return written


def prepare_assessment_dir(base_dir, state_code, asmt_id, mode=0o700):
    directory = os.path.join(base_dir, state_code, asmt_id)
    os.makedirs(directory, mode=mode, exist_ok=True)
    return directory
