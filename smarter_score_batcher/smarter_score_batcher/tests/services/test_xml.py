import unittest
from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from smarter_score_batcher.constants import Constants
from smarter_score_batcher.services import xml
from smarter_score_batcher.celery import setup_celery
from edapi.httpexceptions import EdApiHTTPPreconditionFailed


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

    def test_xml_catcher(self):
        self.__request.json_body = {
            Constants.CONTENT: 'hello'
        }
        response = xml.xml_catcher(self.__request)
        self.assertEqual(response.status_code, 200, "should return 200 after writing xml file")
        with open("/tmp/hello/world/test.xml") as f:
            content = f.read()
        self.assertEqual("hello", content, "xml file should be written to disk")

    def test_xml_catcher_no_content(self):
        self.__request.json_body = {
        }
        self.assertRaises(EdApiHTTPPreconditionFailed, xml.xml_catcher, self.__request)


if __name__ == '__main__':
    unittest.main()
