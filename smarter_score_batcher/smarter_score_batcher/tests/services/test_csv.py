import unittest
import tempfile
import os
import csv
from smarter_score_batcher.utils import meta
from smarter_score_batcher.utils.file_utils import file_writer, create_path

from pyramid.registry import Registry
from pyramid import testing
from smarter_score_batcher.celery import setup_celery
import uuid
from edcore.utils.file_utils import generate_path_to_raw_xml,\
    generate_path_to_item_csv
from smarter_score_batcher.services.csv import create_item_level_csv

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

    def test_create_csv(self):
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
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
        meta_names = meta.Meta(True, 'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8')
        xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
        file_writer(xml_file_path, xml_string)
        create_item_level_csv(root_dir_xml, root_dir_csv, None, meta_names)
        rows = []
        csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
        with open(csv_file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                rows.append(row)
        csv_first_row_list = ['key_value', 'CA-9999999598', 'segmentId_value', 'test', '', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test']
        self.assertEqual(1, len(rows))
        self.assertEqual(csv_first_row_list, rows[0])

if __name__ == "__main__":
    unittest.main()
