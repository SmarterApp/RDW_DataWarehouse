'''
Created on Sep 22, 2014

@author: agrebneva
'''
import unittest
from smarter_score_batcher.templates.asmt_template_manager import MetadataTemplateManager
import os
from smarter_score_batcher.exceptions import MetadataException


class TestJSONMetadata(unittest.TestCase):

    def test_metadata_manager(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../resources/')
        mdm = MetadataTemplateManager(asmt_meta_rel_dir=path)
        self.assertIsNotNone(mdm.get_template('ALIEN'), 'It should find ALIEN template')
        with self.assertRaises(MetadataException):
            mdm.get_template('MATH')
