import unittest
from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from smarter_score_batcher.celery import setup_celery
from unittest.mock import patch
import os
from smarter_score_batcher.services.xml import xml_catcher, process_xml
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
import uuid
import hashlib
import tempfile
from smarter_score_batcher.processors import extract_meta_names
here = os.path.abspath(os.path.dirname(__file__))
xsd_file_path = os.path.abspath(os.path.join(here, '..', '..', '..', 'resources', 'sample_xsd.xsd'))


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

    @patch('smarter_score_batcher.services.xml.extract_meta_names')
    @patch('smarter_score_batcher.services.xml.create_csv')
    @patch('smarter_score_batcher.services.xml.process_xml')
    def test_xml_catcher_succeed(self, mock_process_xml, mock_create_csv, mock_extract_meta_names):
        mock_process_xml.return_value = True
        extract_meta_names.return_value = {'valid_meta': True}
        self.__request.body = '<xml></xml>'
        response = xml_catcher(self.__request)
        self.assertEqual(response.status_code, 200, "should return 200 after writing xml file")

    @patch('smarter_score_batcher.services.xml.process_xml')
    def test_xml_catcher_failed(self, mock_process_xml):
        mock_process_xml.return_value = False
        self.__request.body = '<xml></xml>'
        self.assertRaises(EdApiHTTPPreconditionFailed, xml_catcher, self.__request)

    @patch('smarter_score_batcher.services.xml.process_xml')
    def test_xml_catcher_no_content(self, mock_process_xml):
        mock_process_xml.side_effect = Exception()
        self.__request.body = ''
        self.assertRaises(Exception, xml_catcher, self.__request)

    @patch('smarter_score_batcher.services.xml.create_path')
    def test_process_xml_valid(self, mock_create_path):
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="">
        <ExamineeAttribute context="FINAL" name="StudentIdentifier" value="CA-9999999598" />
        <ExamineeAttribute context="INITIAL" name="StudentIdentifier" value="CA-9999999598" />
        <ExamineeRelationship context="FINAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="FINAL" name="StateName" value="California" />
        <ExamineeRelationship context="INITIAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="INITIAL" name="StateName" value="California" />
        </Examinee>
        </TDSReport>'''
        m1 = hashlib.md5()
        m1.update(bytes(xml_string, 'utf-8'))
        digest1 = m1.digest()
        meta_names = extract_meta_names(xml_string)
        with tempfile.TemporaryDirectory() as tempfolder:
            target = os.path.join(tempfolder, str(uuid.uuid4()), str(uuid.uuid4()))
            mock_create_path.return_value = target

            result_process_xml = process_xml(meta_names, xml_string)
            self.assertTrue(result_process_xml)
            m2 = hashlib.md5()
            with open(target, 'rb') as f:
                m2.update(f.read())
            digest2 = m2.digest()
        self.assertEqual(digest1, digest2)

if __name__ == '__main__':
    unittest.main()
