'''
Created on Jul 15, 2014

@author: agrebneva
'''
import logging
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPServiceUnavailable
from edapi.decorators import validate_xml
from smarter_score_batcher.utils import xsd
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from pyramid.threadlocal import get_current_registry
from edcore.utils.file_utils import generate_path_to_raw_xml,\
    generate_path_to_item_csv
from smarter_score_batcher.tasks.remote_file_writer import remote_write
from smarter_score_batcher.utils.meta import extract_meta_names
from smarter_score_batcher.utils.file_utils import create_path
from smarter_score_batcher.tasks.remote_csv_writer import remote_csv_generator


logger = logging.getLogger("smarter_score_batcher")
xsd_data = xsd.xsd.get_xsd() if xsd.xsd is not None else None


@view_config(route_name='xml', request_method='POST', content_type="application/xml", renderer='json')
@validate_xml(xsd_data)
def xml_catcher(xml_body):
    '''
    XML receiver service expects XML post and will delegate processing based on the root element.
    :param xml_body: xml data
    :returns: http response
    '''
    try:
        meta_names = extract_meta_names(xml_body)
        if not meta_names.valid_meta:
            logger.error('condition of meta_name was not satisfied')
            raise EdApiHTTPPreconditionFailed("Invalid XML")
        settings = get_current_registry().settings
        root_dir_csv = settings.get("smarter_score_batcher.base_dir.csv")
        root_dir_xml = settings.get("smarter_score_batcher.base_dir.xml")
        timeout = int(settings.get("smarter_score_batcher.celery_timeout", 30))
        queue_name = settings.get('smarter_score_batcher.sync_queue')
        succeed = pre_process_xml(meta_names, xml_body, root_dir_xml, queue_name, timeout)
        if succeed:
            # Extract xml for LZ assessment and Item level csv
            queue_name = settings.get('smarter_score_batcher.async_queue')
            post_process_xml(root_dir_xml, root_dir_csv, queue_name, meta_names)
            return Response()
        else:
            return HTTPServiceUnavailable("Writing XML file to disk failed.")
    except Exception as e:
        logger.error(str(e))
        raise


def pre_process_xml(meta_names, raw_xml_string, root_dir_xml, queue_name, timeout):
    '''
    Pre-Process XML (Save it to disk)
    :param meta_names: Meta object
    :param raw_xml_string: xml data
    :param root_dir_xml: xml root directory
    :param queue_name: celery sync queue name
    :param timeout: timeout in second for celery to get result
    :returns" celery response
    '''
    xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
    celery_response = remote_write.apply_async(args=(xml_file_path, raw_xml_string), queue=queue_name)  # @UndefinedVariable
    # wait until file successfully written to disk
    return celery_response.get(timeout=timeout)


def post_process_xml(root_dir_xml, root_dir_csv, queue_name, meta_names):
    '''
    Post-Process XML by call celery task to process xml for assessment and item level
    :param root_dir_xml: xml root directory
    :param root_dir_csv: csv root directory
    :param queue_name: celery sync queue name
    :param meta_names: Meta object
    :returns: celery response
    '''
    xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
    csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
    return remote_csv_generator.apply_async(args=(csv_file_path, xml_file_path), queue=queue_name)      # @UndefinedVariable
