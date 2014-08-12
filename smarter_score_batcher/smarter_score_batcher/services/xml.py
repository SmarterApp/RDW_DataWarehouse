'''
Created on Jul 15, 2014

@author: agrebneva
'''
import logging
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPServiceUnavailable
from smarter_score_batcher.processors import process_xml
from smarter_score_batcher.processors import create_csv
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from edapi.decorators import validate_xml
from smarter_score_batcher.utils import xsd


logger = logging.getLogger("smarter_score_batcher")
xsd_data = xsd.xsd.get_xsd() if xsd.xsd is not None else None


@view_config(route_name='xml', request_method='POST', content_type="application/xml", renderer='json')
@validate_xml(xsd_data)
def xml_catcher(xml_body):
    """
    XML cacther service expects XML post and will delegate processing based on the root element.
    """
    try:
        succeed = process_xml(xml_body)
        if succeed:
            #create csv asynchronous
            create_csv(xml_body)
            return Response()
        else:
            return HTTPServiceUnavailable("Writing XML file to disk failed.")
    except Exception as e:
        logger.error(str(e))
        raise
