import unittest
import DataGeneration.src.writers.write_to_csv as write_to_csv
import os
from DataGeneration.src.models.entities import Assessment


class TestWriteToCSV(unittest.TestCase):

    def setUp(self):
        self.current_file_path = os.path.dirname(os.path.realpath(__file__))

    def test_create_csv(self):
        asmt_1 = Assessment(1, 'guid_1', 'summative', '2013', '2013', 'V1', 'subject1', 3, '01/01/13', True)
        asmt_2 = Assessment(2, 'guid_2', 'summative', '2013', '2013', 'V1', 'subject2', 1, '01/01/13', True)
        entity_list = [asmt_1, asmt_2]
        filename = os.path.join(self.current_file_path, 'test_data', 'test_create_csv.csv')
        open(filename, 'w').close()

        write_to_csv.create_csv(entity_list, filename)

        expected_lines = ['1,guid_1,summative,2013,2013,V1,subject1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,01/01/13,,True',
                          '2,guid_2,summative,2013,2013,V1,subject2,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,01/01/13,,True']
        actual_lines = self._read_file(filename)

        # verify
        self.assertEqual(len(actual_lines), len(expected_lines))
        for i in range(len(actual_lines)):
            self.assertEqual(actual_lines[0].strip('\r\n'), expected_lines[0].strip('\r\n'))

        # delete file
        os.remove(filename)

    def test_clear_files(self):
        # prepare data
        entity_to_path_dict = {DummyInstitutionHierarchy: os.path.join(self.current_file_path, 'test_data', 'test_dim_inst_hier.csv'),
                               DummyAssessmentOutcome: os.path.join(self.current_file_path, 'test_data', 'test_fact_asmt_outcome.csv')}
        self._write_into_file(list(entity_to_path_dict.values()))
        # verify files are not empty
        for file in list(entity_to_path_dict.values()):
            self.assertTrue(len(self._read_file(file)) > 0)

        write_to_csv.clear_files(entity_to_path_dict)

        # verify files are empty
        for file in list(entity_to_path_dict.values()):
            self.assertEqual(len(self._read_file(file)), 0)

        # clear files
        for file in list(entity_to_path_dict.values()):
            os.remove(file)

    def _read_file(self, filename):
        with open(filename) as f:
            content = f.readlines()
        return content

    def _write_into_file(self, files):
        for file in files:
            with open(file, 'w') as test_file:
                test_file.write('test data\n')


class DummyInstitutionHierarchy(object):
    pass


class DummyAssessmentOutcome(object):
    pass
