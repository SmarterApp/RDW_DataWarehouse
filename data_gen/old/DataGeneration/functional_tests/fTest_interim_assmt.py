'''
Created on Dec 5, 2013

@author: bpatel
'''
import unittest
import tempfile
import shutil
import os
import subprocess
import csv
import json
import glob
import time

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
TEST_SUMMATIVE_CSV = os.path.join(__location__, '..', 'datafiles', 'test_interim_assmt.csv')
TEST_SUMMATIVE_JSON = os.path.join(__location__, '..', 'datafiles', 'test_interim_assmt.json')
guid_asmt = 'guid_asmt'
asmt_type = 'asmt_type'
score_asmt = 'score_asmt'
MIN = int('1200')
MAX = int('2400')


class functionaltest(unittest.TestCase):
# Create tmp unique dir
    def setUp(self):
        self.interim_file_dir = tempfile.mkdtemp()
        self.assertTrue(os.path.exists(self.interim_file_dir))

# Delete tmp dir
    def tearDown(self):
        shutil.rmtree(self.interim_file_dir)

#generate interim files based on given summative files, store the output in tmpp dir and interim data will be exactly 30 pt off.
    def generate_interim_assmt(self):
        print(self.interim_file_dir)
        print(__location__)
        command = 'python -m DataGeneration.src.additional_asmt_generator -c {csv} -j {json} -a INTERIM -o {dirname} -l {score_change_min} -u {score_change_max}'
        command = command.format(dirname=self.interim_file_dir, csv=TEST_SUMMATIVE_CSV, json=TEST_SUMMATIVE_JSON, score_change_min=30, score_change_max=30)
        subprocess.call(command, shell=True)

#compare given summative csv and interim csv.
    def compare_both_csv(self):
        print('*******')
        print(self.interim_file_dir)
        time.sleep(3)
        interim_csv = glob.glob(os.path.join(self.interim_file_dir, 'REALDATA_ASMT_ID_*.csv'))
        print(interim_csv)

        with open(TEST_SUMMATIVE_CSV, 'r') as old:
            with open(interim_csv[0], 'r') as new:
                old_csv = csv.DictReader(old)
                new_csv = csv.DictReader(new)
                for old_row in old_csv:
                    new_row = next(new_csv)

                    # Verify guid_asmt is different in Inerim and Summative csv
                    self.assertNotEqual(old_row[guid_asmt], new_row[guid_asmt])

                    # Verify asmt_types is INTERIM
                    self.assertEquals(new_row[asmt_type], 'INTERIM')
                    #Actual score of interim data is less than 30 (offset) but if the new score is less than 1200 it will
                    #retun MIN and if it is more than 2400 it will return MAX.
                    old_data = int(old_row[score_asmt]) - 30
                    if old_data < MIN:
                        old_data = MIN
                    elif old_data > MAX:
                        old_data = MAX
                    self.assertEquals(int(new_row[score_asmt]), old_data)

    def test_validate_interim_assmt(self):
        self.generate_interim_assmt()
        self.compare_both_csv()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
