'''
Created on Aug 12, 2014

@author: tosako
'''
from smarter_score_batcher.processors import create_path
from pyramid.threadlocal import get_current_registry
from edcore.utils.file_utils import generate_path_to_raw_xml,\
    generate_path_to_item_csv
from smarter_score_batcher.tasks.remote_csv_writer import remote_csv_generator


def create_csv(meta_names):
    settings = get_current_registry().settings
    root_dir_csv = settings.get("smarter_score_batcher.base_dir.csv")
    root_dir_xml = settings.get("smarter_score_batcher.base_dir.xml")
    # TODO:  We need the async queue
    queue_name = settings.get('smarter_score_batcher.sync_queue')
    xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
    csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
    celery_response = remote_csv_generator.apply_async(args=(csv_file_path, xml_file_path), queue=queue_name)     # @UndefinedVariable
    return celery_response
