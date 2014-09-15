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