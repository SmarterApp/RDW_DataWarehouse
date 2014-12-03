'''
Created on Sep 22, 2014

@author: agrebneva
'''
import unittest
from smarter_score_batcher.templates.asmt_template_manager import MetadataTemplateManager,\
    PerfMetadataTemplateManager, get_template_key
import os
from smarter_score_batcher.error.exceptions import MetadataException
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


class TestAsmtMetadata(unittest.TestCase):

    def setUp(self):
        CacheManager(**parse_cache_config_options({'cache.regions': 'public.shortlived', 'cache.type': 'memory', 'cache.public.shortlived.expire': 7200}))

    def test_static_metadata_manager(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../resources/meta/static')
        mdm = MetadataTemplateManager(asmt_meta_dir=path)
        self.assertIsNotNone(mdm.get_template('ALIEN'), 'It should find ALIEN template')
        with self.assertRaises(MetadataException):
            mdm.get_template('SOMETHING_MISSING')

    def test_performance_metadata_manager(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../resources/meta/performance')
        static_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../resources/meta/static')
        mdm = PerfMetadataTemplateManager(asmt_meta_dir=path, static_asmt_meta_dir=static_path)
        self.assertIsNotNone(mdm.get_template(get_template_key(2015, 'summative', 3, 'ALIEN')), 'It should find ALIEN template for 3rd grade')
        tmpl = mdm.get_template(get_template_key(2015, 'summative', 8, 'ALIEN'))
        self.assertIsNotNone(tmpl, 'It should find ALIEN template for 8th grade')
        self.assertEqual(tmpl['Overall']['MinScore'], '1000')
        self.assertEqual(tmpl['Claims']['Claim1']['Name'], 'Alien Name')
        with self.assertRaises(MetadataException):
            mdm.get_template(get_template_key(2015, 'summative', 11, 'MATH'))

    def test_default_metadata_manager(self):
        perf_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../resources/bad_meta/performance')
        static_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../resources/meta/static')
        default_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../resources/meta/default')
        mdm = PerfMetadataTemplateManager(asmt_meta_dir=perf_path, static_asmt_meta_dir=static_path, default_asmt_meta_dir=default_path)
        self.assertIsNotNone(mdm.get_template(get_template_key(2015, 'interim assessment blocks', 3, 'MATH')), 'It should find math template for 3rd grade')
        tmpl = mdm.get_template(get_template_key(2015, 'interim assessment blocks', 8, 'Math'))
        # all values should be from default json
        self.assertIsNotNone(tmpl, 'It should find math template for 8th grade')
        self.assertEqual(tmpl['Overall']['MinScore'], 0)
        self.assertEqual(tmpl['Claims']['Claim1']['Name'], '')
        # MetadataException should be raised if no default JSON can be found for give assessment type
        with self.assertRaises(MetadataException):
            mdm.get_template(get_template_key(2015, 'summative', 11, 'MATH'))
