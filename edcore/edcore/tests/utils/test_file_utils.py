import os
from unittest import TestCase
from edcore.utils.file_utils import generate_file_path, \
    generate_path_to_item_csv, generate_path_to_raw_xml


class TestFileUtils(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generate_path(self):
        items_root_dir = os.path.dirname(os.path.abspath(__file__))
        record = {}
        extension = "csv"
        path = generate_file_path(items_root_dir, extension, **record)
        self.assertEqual(path, items_root_dir + '.' + extension)

        record = {'state_code': 'NC'}
        path = generate_file_path(items_root_dir, extension, **record)
        expect_path = os.path.join(items_root_dir, 'NC')
        self.assertEqual(path, expect_path + '.' + extension)

        record['asmt_year'] = 2015
        path = generate_file_path(items_root_dir, extension, **record)
        expect_path = os.path.join(expect_path, '2015')
        self.assertEqual(path, expect_path + '.' + extension)

        record['asmt_type'] = 'SUMMATIVE'
        path = generate_file_path(items_root_dir, extension, **record)
        expect_path = os.path.join(expect_path, 'SUMMATIVE')
        self.assertEqual(path, expect_path + '.' + extension)

        record['effective_date'] = 20150402
        path = generate_file_path(items_root_dir, extension, **record)
        expect_path = os.path.join(expect_path, '20150402')
        self.assertEqual(path, expect_path + '.' + extension)

        record['asmt_subject'] = 'Math'
        path = generate_file_path(items_root_dir, extension, **record)
        expect_path = os.path.join(expect_path, 'MATH')
        self.assertEqual(path, expect_path + '.' + extension)

        record['asmt_grade'] = 3
        path = generate_file_path(items_root_dir, extension, **record)
        expect_path = os.path.join(expect_path, '3')
        self.assertEqual(path, expect_path + '.' + extension)

        record['district_id'] = '3ab54de78a'
        path = generate_file_path(items_root_dir, extension, **record)
        expect_path = os.path.join(expect_path, '3ab54de78a')
        self.assertEqual(path, expect_path + '.' + extension)

        record['student_id'] = 'a78dbf34'
        path = generate_file_path(items_root_dir, extension, **record)
        expect_path = os.path.join(expect_path, 'a78dbf34.csv')
        self.assertEqual(path, expect_path)

    def test_generate_path_for_raw_xml(self):
        items_root_dir = os.path.dirname(os.path.abspath(__file__))
        record = {}
        record = {'state_code': 'NC'}
        record['asmt_year'] = 2015
        record['asmt_type'] = 'SUMMATIVE'
        record['asmt_subject'] = 'Math'
        record['asmt_grade'] = 3
        record['district_id'] = '3ab54de78a'
        record['student_id'] = 'a78dbf34'
        path = generate_path_to_raw_xml(items_root_dir, **record)
        expect_path = os.path.join(items_root_dir, "NC/2015/SUMMATIVE/MATH/3/3ab54de78a/a78dbf34.xml")
        self.assertEqual(path, expect_path)

        record['effective_date'] = 20150402
        path = generate_path_to_raw_xml(items_root_dir, **record)
        expect_path = os.path.join(items_root_dir, "NC/2015/SUMMATIVE/20150402/MATH/3/3ab54de78a/a78dbf34.xml")
        self.assertEqual(path, expect_path)

    def test_generate_path_for_item_level_csv(self):
        items_root_dir = os.path.dirname(os.path.abspath(__file__))
        record = {}
        record = {'state_code': 'NC'}
        record['asmt_year'] = 2015
        record['asmt_type'] = 'SUMMATIVE'
        record['effective_date'] = 20150402
        record['asmt_subject'] = 'Math'
        record['asmt_grade'] = 3
        record['district_id'] = '3ab54de78a'
        record['student_id'] = 'a78dbf34'
        path = generate_path_to_item_csv(items_root_dir, **record)
        expect_path = os.path.join(items_root_dir, "NC/2015/SUMMATIVE/20150402/MATH/3/3ab54de78a/a78dbf34.csv")
        self.assertEqual(path, expect_path)
