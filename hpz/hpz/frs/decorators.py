# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
