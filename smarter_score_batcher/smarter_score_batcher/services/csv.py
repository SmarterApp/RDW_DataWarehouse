'''
Created on Aug 12, 2014

@author: tosako
'''
from smarter_score_batcher.processors import extract_meta_names, create_path
from pyramid.threadlocal import get_current_registry
from edcore.utils.file_utils import generate_path_to_raw_xml,\
    generate_path_to_item_csv
from smarter_score_batcher.tasks.remote_csv_writer import remote_csv_generator


def create_csv(raw_xml_string):
    meta_names = extract_meta_names(raw_xml_string)
    settings = get_current_registry().settings
    root_dir_csv = settings.get("smarter_score_batcher.base_dir.csv")
    root_dir_xml = settings.get("smarter_score_batcher.base_dir.xml")
    xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
    csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
    queue_name = settings.get('smarter_score_batcher.sync_queue')
    args = (csv_file_path, xml_file_path)
    celery_response = remote_csv_generator.apply_async(args=args, queue=queue_name)
    return celery_response