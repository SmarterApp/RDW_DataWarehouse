'''
Created on Oct 3, 2014

@author: tosako
'''
import unittest
from smarter_score_batcher.utils.performance_metadata_generator import PerformanceMetadata, \
    _format_performance_metadata, generate_performance_metadata
from smarter_score_batcher.utils.constants import PerformanceMetadataConstants
from smarter_score_batcher.error.exceptions import MetadataException
import os
import json


class Test(unittest.TestCase):

    def test_PerformanceMetadata_min_value(self):
        performanceMetadata = PerformanceMetadata()
        performanceMetadata.set_overall_minScore(1000)
        performanceMetadata.set_overall_minScore(100)
        performanceMetadata.set_overall_minScore(300)
        self.assertEqual(100, performanceMetadata.get_overall_minScore())

    def test_PerformanceMetadata_max_value(self):
        performanceMetadata = PerformanceMetadata()
        performanceMetadata.set_overall_maxScore(1000)
        performanceMetadata.set_overall_maxScore(100)
        performanceMetadata.set_overall_maxScore(300)
        self.assertEqual(1000, performanceMetadata.get_overall_maxScore())

    def test_claim_min_max_score(self):
        performanceMetadata = PerformanceMetadata()
        performanceMetadata.set_overall_minScore(1000)
        performanceMetadata.set_overall_minScore(100)
        performanceMetadata.set_overall_minScore(300)
        performanceMetadata.set_overall_maxScore(1000)
        performanceMetadata.set_overall_maxScore(100)
        performanceMetadata.set_overall_maxScore(300)
        self.assertEqual(0, performanceMetadata.get_claim1_minScore())
        self.assertEqual(0, performanceMetadata.get_claim1_maxScore())
        self.assertEqual(0, performanceMetadata.get_claim2_minScore())
        self.assertEqual(0, performanceMetadata.get_claim2_maxScore())
        self.assertEqual(0, performanceMetadata.get_claim3_minScore())
        self.assertEqual(0, performanceMetadata.get_claim3_maxScore())
        self.assertEqual(0, performanceMetadata.get_claim4_maxScore())
        self.assertEqual(0, performanceMetadata.get_claim4_minScore())

    def test_format_performance_metadata(self):
        performanceMetadata = PerformanceMetadata()
        meta = _format_performance_metadata(performanceMetadata)
        keys = meta.keys()
        self.assertEqual(4, len(keys))
        self.assertIn(PerformanceMetadataConstants.IDENTIFICATION, keys)
        self.assertIn(PerformanceMetadataConstants.PERFORMANCELEVELS, keys)
        self.assertIn(PerformanceMetadataConstants.CLAIMS, keys)
        self.assertIn(PerformanceMetadataConstants.OVERALL, keys)

        identification = meta[PerformanceMetadataConstants.IDENTIFICATION]
        keys = identification.keys()
        self.assertEqual(1, len(keys))
        self.assertIn(PerformanceMetadataConstants.SUBJECT, keys)

        claims = meta[PerformanceMetadataConstants.CLAIMS]
        keys = claims.keys()
        self.assertEqual(4, len(keys))
        self.assertIn(PerformanceMetadataConstants.CLAIM1, keys)
        self.assertIn(PerformanceMetadataConstants.CLAIM2, keys)
        self.assertIn(PerformanceMetadataConstants.CLAIM3, keys)
        self.assertIn(PerformanceMetadataConstants.CLAIM4, keys)

        for i in range(1, len(claims) + 1):
            claim = claims['Claim' + str(i)]
            keys = claim.keys()
            self.assertEqual(2, len(claim))
            self.assertIn(PerformanceMetadataConstants.MAXSCORE, keys)
            self.assertIn(PerformanceMetadataConstants.MINSCORE, keys)

        performancelevels = meta[PerformanceMetadataConstants.PERFORMANCELEVELS]
        keys = performancelevels.keys()
        self.assertEqual(4, len(performancelevels))
        self.assertIn(PerformanceMetadataConstants.LEVEL1, keys)
        self.assertIn(PerformanceMetadataConstants.LEVEL2, keys)
        self.assertIn(PerformanceMetadataConstants.LEVEL3, keys)
        self.assertIn(PerformanceMetadataConstants.LEVEL4, keys)
        for i in range(1, len(performancelevels) + 1):
            cutpoint = performancelevels['Level' + str(i)]
            keys = cutpoint.keys()
            self.assertEqual(1, len(cutpoint))
            self.assertIn(PerformanceMetadataConstants.CUTPOINT, keys)

        overall = meta[PerformanceMetadataConstants.OVERALL]
        keys = overall.keys()
        self.assertEqual(2, len(overall))
        self.assertIn(PerformanceMetadataConstants.MAXSCORE, keys)
        self.assertIn(PerformanceMetadataConstants.MINSCORE, keys)

    def test_generate_performance_metadata_invalid_filepath(self):
        filepath = '/foo/wrong_file.xml'
        self.assertRaises(MetadataException, generate_performance_metadata, filepath)

    def test_generate_performance_metadata_invalid_value(self):
        here = os.path.abspath(os.path.dirname(__file__))
        xml_path = os.path.join(here, '..', 'resources', 'bad_meta', 'ELA.asmt_metadata.invalid_value_in_performance.xml')
        self.assertTrue(os.path.exists(xml_path))
        self.assertRaises(MetadataException, generate_performance_metadata, xml_path)

    def test_generate_performance_metadata(self):
        here = os.path.abspath(os.path.dirname(__file__))
        xml_path = os.path.join(here, '..', 'resources', 'meta', 'performance', '2014', 'summative', '3', 'ELA.asmt_metadata.xml')
        self.assertTrue(os.path.exists(xml_path))
        with open(xml_path) as f:
            j = f.read()
        meta = generate_performance_metadata(j)
        self.assertEqual('ELA', meta[PerformanceMetadataConstants.IDENTIFICATION][PerformanceMetadataConstants.SUBJECT])
        self.assertEqual('0', meta[PerformanceMetadataConstants.CLAIMS][PerformanceMetadataConstants.CLAIM2][PerformanceMetadataConstants.MAXSCORE])
        self.assertEqual('0', meta[PerformanceMetadataConstants.CLAIMS][PerformanceMetadataConstants.CLAIM2][PerformanceMetadataConstants.MINSCORE])
        self.assertEqual('1000', meta[PerformanceMetadataConstants.PERFORMANCELEVELS][PerformanceMetadataConstants.LEVEL1][PerformanceMetadataConstants.CUTPOINT])
        self.assertEqual('1200', meta[PerformanceMetadataConstants.PERFORMANCELEVELS][PerformanceMetadataConstants.LEVEL2][PerformanceMetadataConstants.CUTPOINT])
        self.assertEqual('1500', meta[PerformanceMetadataConstants.PERFORMANCELEVELS][PerformanceMetadataConstants.LEVEL3][PerformanceMetadataConstants.CUTPOINT])
        self.assertEqual('2000', meta[PerformanceMetadataConstants.PERFORMANCELEVELS][PerformanceMetadataConstants.LEVEL4][PerformanceMetadataConstants.CUTPOINT])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
