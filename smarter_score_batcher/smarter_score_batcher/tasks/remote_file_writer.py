'''
Created on Jul 28, 2014

@author: tosako
'''


import logging
from smarter_score_batcher.celery import celery, conf
from smarter_score_batcher.utils.file_utils import file_writer, create_path
from smarter_score_batcher.utils.meta import extract_meta_names
from edcore.utils.file_utils import generate_path_to_item_csv, generate_file_path
from smarter_score_batcher.tasks.remote_csv_writer import remote_csv_generator
from pyramid.threadlocal import get_current_registry
import time
from smarter_score_batcher.error.exceptions import TSBException

logger = logging.getLogger("smarter_score_batcher")


@celery.task(name="tasks.tsb.remote_file_writer")
def remote_write(xml_data):
    '''
    save data in given path
    :returns: True when file is written
    '''
    written = False
    try:
        meta_names = extract_meta_names(xml_data)

        if conf is None or not conf:
            # maybe service is eager mode. If so, read from registry
            settings = get_current_registry().settings
            if settings is not None:
                global conf
                conf = settings

        root_dir_csv = conf.get("smarter_score_batcher.base_dir.csv")
        root_dir_xml = conf.get("smarter_score_batcher.base_dir.xml")
        timestamp = time.strftime('%Y%m%d%H%M%S', time.gmtime())
        xml_file_path = create_path(root_dir_xml, meta_names, generate_file_path, **{'extension': timestamp + '.xml'})
        written = file_writer(xml_file_path, xml_data)
        if written:
            work_dir = conf.get("smarter_score_batcher.base_dir.working")
            queue_name = conf.get('smarter_score_batcher.async_queue')
            csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
            remote_csv_generator.apply_async(args=(meta_names, csv_file_path, xml_file_path, work_dir), queue=queue_name)  # @UndefinedVariable
    except TSBException:
        # ignore exception for error handling because this function is synchonous call
        pass
    return written
