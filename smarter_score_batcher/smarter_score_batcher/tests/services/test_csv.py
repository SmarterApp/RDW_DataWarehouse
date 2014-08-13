import unittest
import tempfile
import os
import csv
from smarter_score_batcher.services import csv as Csv
from smarter_score_batcher.utils import meta
from smarter_score_batcher.utils.file_utils import file_writer

from pyramid.registry import Registry
from pyramid import testing
from smarter_score_batcher.celery import setup_celery
from unittest.mock import patch
import uuid

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Test(unittest.TestCase):
    def setUp(self):
        self.__tempfolder = tempfile.TemporaryDirectory()
        # setup registry
        settings = {
            'smarter_score_batcher.celery_timeout': 30,
            'smarter_score_batcher.celery.celery_always_eager': True,
            'smarter_score_batcher.base_dir': self.__tempfolder.name
        }
        reg = Registry()
        reg.settings = settings
        self.__config = testing.setUp(registry=reg)
        setup_celery(settings)

    def tearDown(self):
        self.__tempfolder.cleanup()
        testing.tearDown()

    @patch('smarter_score_batcher.services.csv.create_path')
    def test_create_csv(self, mock_create_path):
        target1 = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        target2 = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        mock_create_path.side_effect = [target1, target2]
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
        <Opportunity>
        <Item position="test" segmentId="segmentId_value"
        bankKey="test" key="key_value" operational="test" isSelected="test" format="test"
        score="test" scoreStatus="test" adminDate="test" numberVisits="test"
        mimeType="test" strand="test" contentLevel="test" pageNumber="test" pageVisits="test"
        pageTime="test" dropped="test">
        </Item>
        </Opportunity>
        </TDSReport>'''
        file_writer(target1, xml_string)
        meta_names = meta.Meta(True, 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test')
        Csv.create_csv(None, None, None, meta_names)
        with open(target2, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                first_row = row
        csv_first_row_list = ['key_value', 'CA-9999999598', 'segmentId_value', 'test', '', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test']
        self.assertEqual(csv_first_row_list, first_row)

if __name__ == "__main__":
    unittest.main()
