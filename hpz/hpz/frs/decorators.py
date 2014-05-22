from functools import wraps
import json
import logging
from pyramid.response import Response

__author__ = 'ablum'

logger = logging.getLogger(__name__)


def validate_request_info(parameter, *fields):

    def request_wrap(request_handler):

        @wraps(request_wrap)
        def validate_wrap(*args, **kwds):
            context, request = args
            request_fields = getattr(request, parameter)
            for field in fields:
                if field not in request_fields:
                    logger.error('The request does not contain %s, rejecting request' % field)
                    return Response(body=json.dumps({}))

            return request_handler(*args, **kwds)

        return validate_wrap

    return request_wrap
