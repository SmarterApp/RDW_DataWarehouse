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

import logging
import unittest
from unittest import mock
from hpz.frs import decorators
from hpz.frs.decorators import validate_request_info
from pyramid.testing import DummyRequest
from hpz.tests.unit_tests.frs.test_upload_service import DummyFile


__author__ = 'ablum'

VALID_HEADER = 'valid_header'
INVALID_HEADER = 'invalid_header'


class DecoratorsTest(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()

    def test_valid_headers(self):
        self.__request.headers = {VALID_HEADER: '1234'}
        result = dummy_headers_function(None, self.__request)
        self.assertTrue('SUCCESS', result)

    def test_invalid_headers(self):
        self.__request.headers = {INVALID_HEADER: '1234'}
        test_logger = logging.getLogger(decorators.__name__)
        with mock.patch.object(test_logger, 'error') as mock_error:
            result = dummy_headers_function(None, self.__request)
            self.assertTrue(200, result.status)
            self.assertTrue(mock_error.called)

    def test_valid_post_body(self):
        self.__request.POST['file'] = DummyFile()
        result = dummy_postbody_function(None, self.__request)
        self.assertTrue('SUCCESS', result)

    def test_invalid_post_body(self):
        self.__request.POST['wrong_file'] = DummyFile()
        test_logger = logging.getLogger(decorators.__name__)
        with mock.patch.object(test_logger, 'error') as mock_error:
            result = dummy_postbody_function(None, self.__request)
            self.assertTrue(200, result.status)
            self.assertTrue(mock_error.called)


@validate_request_info('headers', VALID_HEADER)
def dummy_headers_function(context, request):
    return 'SUCCESS'


@validate_request_info('POST', VALID_HEADER)
def dummy_postbody_function(context, request):
    return 'SUCCESS'
