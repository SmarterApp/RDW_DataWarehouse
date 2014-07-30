'''
Created on Jul 15, 2014

@author: agrebneva
'''
import logging
from pyramid.view import view_config
from pyramid.response import Response
from smarter_score_batcher.processors import process_tdsreport
from edapi.decorators import validate_params

logger = logging.getLogger(__name__)

XML_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "content": "string",
        "required": True,
    }
}


@view_config(route_name='xml', request_method='POST', content_type="application/json")
@validate_params(schema=XML_PARAMS)
def xml_catcher(context, request):
    """ XML cacther service expects XML post and will delegate processing based on the root element.
    """
    try:
        process_tdsreport(request.body)
    except Exception as e:
        logger.error(str(e))
        raise
    else:
        return Response('OK')
