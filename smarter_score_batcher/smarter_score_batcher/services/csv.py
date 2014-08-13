'''
Created on Aug 12, 2014

@author: tosako
'''
import logging
from edcore.utils.file_utils import generate_path_to_raw_xml,\
    generate_path_to_item_csv
from smarter_score_batcher.tasks.remote_csv_writer import remote_csv_generator
from smarter_score_batcher.utils.file_utils import create_path


logger = logging.getLogger("smarter_score_batcher")


def create_csv(root_dir_csv, root_dir_xml, meta_names, queue_name):
    '''
    Call celery task to process xml for assessment and item level
    '''
    xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
    csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
    return remote_csv_generator.apply_async(args=(csv_file_path, xml_file_path), queue=queue_name)     # @UndefinedVariable
