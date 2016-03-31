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

'''
Created on Sep 12, 2014

@author: tosako
'''
import unittest
from unittest.mock import patch
import requests.exceptions as req_exc
from edcore.notification.callback import post_notification
from edcore.notification.constants import Constants


class Test(unittest.TestCase):
    @patch('edcore.notification.callback.post')
    def test_post_notification_connection_error(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = req_exc.ConnectionError('hello')
        notification_status, notification_error = post_notification(None, None, None)
        self.assertEqual(notification_status, Constants.PENDING)
        self.assertEqual(notification_error, 'hello')

    @patch('edcore.notification.callback.post')
    def test_post_notification_Timeout(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = req_exc.Timeout('hello')
        notification_status, notification_error = post_notification(None, None, None)
        self.assertEqual(notification_status, Constants.PENDING)
        self.assertEqual(notification_error, 'hello')

    @patch('edcore.notification.callback.post')
    def test_post_notification_HTTPError_408(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = req_exc.HTTPError('hello')
        mock_post.return_value.status_code = 408
        notification_status, notification_error = post_notification(None, None, None)
        self.assertEqual(notification_status, Constants.PENDING)
        self.assertEqual(notification_error, 'hello')

    @patch('edcore.notification.callback.post')
    def test_post_notification_HTTPError(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = req_exc.HTTPError('hello')
        notification_status, notification_error = post_notification(None, None, None)
        self.assertEqual(notification_status, Constants.FAILURE)
        self.assertEqual(notification_error, 'hello')

    @patch('edcore.notification.callback.post')
    def test_post_notification_RequestException(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = req_exc.Timeout('hello')
        notification_status, notification_error = post_notification(None, None, None)
        self.assertEqual(notification_status, Constants.PENDING)
        self.assertEqual(notification_error, 'hello')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_post_notification']
    unittest.main()
