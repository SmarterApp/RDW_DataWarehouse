'''
Created on Jul 15, 2014

@author: agrebneva
'''
import logging
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPServiceUnavailable
from edapi.decorators import validate_params
from smarter_score_batcher.processors import process_xml
from smarter_score_batcher.constants import Constants


logger = logging.getLogger("smarter_score_batcher")


XML_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        Constants.CONTENT: "string",
        "required": True
    }
}


@view_config(route_name='xml', request_method='POST', content_type="application/json", renderer='json')
# @validate_params(schema=XML_PARAMS)
def xml_catcher(request):
    """ XML cacther service expects XML post and will delegate processing based on the root element.
    """
    try:
        params = request.json_body
        xml_body = params.get(Constants.CONTENT)
        succeed = process_xml(xml_body)
        if succeed:
            return Response()
        else:
            return HTTPServiceUnavailable("Writing XML file to disk failed.")
    except Exception as e:
        logger.error(str(e))
        raise
