import unittest
from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from smarter_score_batcher.services import xml
from smarter_score_batcher.celery import setup_celery
from unittest.mock import patch


class TestXML(unittest.TestCase):

    def setUp(self):
        # setup request
        self.__request = DummyRequest()
        self.__request.method = 'POST'
        # setup registry
        settings = {
            'smarter_score_batcher.celery_timeout': 30,
            'smarter_score_batcher.celery.celery_always_eager': True
        }
        reg = Registry()
        reg.settings = settings
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        setup_celery(settings)

    def tearDown(self):
        testing.tearDown()

    @patch('smarter_score_batcher.services.xml.process_xml')
    def test_xml_catcher_succeed(self, mock_process_xml):
        mock_process_xml.return_value = True
        self.__request.body = '<xml></xml>'
        response = xml.xml_catcher(self.__request)
        self.assertEqual(response.status_code, 200, "should return 200 after writing xml file")

    @patch('smarter_score_batcher.services.xml.process_xml')
    def test_xml_catcher_failed(self, mock_process_xml):
        mock_process_xml.return_value = False
        self.__request.body = '<xml></xml>'
        response = xml.xml_catcher(self.__request)
        self.assertEqual(response.status_code, 503, "should return 200 after writing xml file")

    @patch('smarter_score_batcher.services.xml.process_xml')
    def test_xml_catcher_no_content(self, mock_process_xml):
        mock_process_xml.side_effect = Exception()
        self.__request.body = ''
        self.assertRaises(Exception, xml.xml_catcher, self.__request)


if __name__ == '__main__':
    unittest.main()
