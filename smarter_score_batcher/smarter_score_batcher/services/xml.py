'''
Created on Jul 15, 2014

@author: agrebneva
'''
import logging
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPServiceUnavailable
from smarter_score_batcher.processors import process_xml
from edapi.httpexceptions import EdApiHTTPPreconditionFailed


logger = logging.getLogger("smarter_score_batcher")


@view_config(route_name='xml', request_method='POST', content_type="application/xml", renderer='json')
def xml_catcher(request):
    """
    XML cacther service expects XML post and will delegate processing based on the root element.
    """
    try:
        xml_body = request.body
        succeed = process_xml(xml_body)
        if succeed:
            return Response()
        else:
            return HTTPServiceUnavailable("Writing XML file to disk failed.")
    except EdApiHTTPPreconditionFailed as e:
        # return error code 412
        return e
    except Exception as e:
        logger.error(str(e))
        raise
