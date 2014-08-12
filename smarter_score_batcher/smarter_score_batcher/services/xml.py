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
from smarter_score_batcher.services.csv import create_csv
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from pyramid.threadlocal import get_current_registry
from edcore.utils.file_utils import generate_path_to_raw_xml
from smarter_score_batcher.tasks.remote_file_writer import remote_write
from smarter_score_batcher.utils.meta import extract_meta_names
from smarter_score_batcher.utils.file_utils import create_path


logger = logging.getLogger("smarter_score_batcher")
xsd_data = xsd.xsd.get_xsd() if xsd.xsd is not None else None


@view_config(route_name='xml', request_method='POST', content_type="application/xml", renderer='json')
@validate_xml(xsd_data)
def xml_catcher(xml_body):
    '''
    XML receiver service expects XML post and will delegate processing based on the root element.
    '''
    try:
        meta_names = extract_meta_names(xml_body)
        if not meta_names.valid_meta:
            raise EdApiHTTPPreconditionFailed("Invalid XML")
        succeed = process_xml(meta_names, xml_body)
        if succeed:
            #create csv asynchronous
            create_csv(meta_names)
            return Response()
        else:
            return HTTPServiceUnavailable("Writing XML file to disk failed.")
    except Exception as e:
        logger.error(str(e))
        raise


def process_xml(meta_names, raw_xml_string):
    '''
    Process tdsreport doc
    '''
    settings = get_current_registry().settings
    root_dir = settings.get("smarter_score_batcher.base_dir.xml")
    timeout = settings.get("smarter_score_batcher.celery_timeout", 30)
    queue_name = settings.get('smarter_score_batcher.sync_queue')
    xml_file_path = create_path(root_dir, meta_names, generate_path_to_raw_xml)
    celery_response = remote_write.apply_async(args=(xml_file_path, raw_xml_string), queue=queue_name)  # @UndefinedVariable
    # wait until file successfully written to disk
    return celery_response.get(timeout=timeout)
