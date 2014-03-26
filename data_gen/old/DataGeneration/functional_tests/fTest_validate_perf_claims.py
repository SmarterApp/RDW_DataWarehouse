'''
Created on Dec 30, 2013

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

CLAIM_SCORE_CUT_PT1 = '1600'
CLAIM_SCORE_CUT_PT2 = '2000'
CLAIM_SCORE_CUT_PT3 = '2400'
asmt_claim_1_score = 'asmt_claim_1_score'
asmt_claim_1_perf_lvl = 'asmt_claim_1_perf_lvl'
asmt_claim_2_score = 'asmt_claim_2_score'
asmt_claim_2_perf_lvl = 'asmt_claim_2_perf_lvl'
asmt_claim_3_score = 'asmt_claim_3_score'
asmt_claim_3_perf_lvl = 'asmt_claim_3_perf_lvl'
asmt_claim_4_score = 'asmt_claim_4_score'
asmt_claim_4_perf_lvl = 'asmt_claim_4_perf_lvl'
asmt_claim_perf_lvl_name_1 = 'asmt_claim_perf_lvl_name_1'
asmt_claim_perf_lvl_name_2 = 'asmt_claim_perf_lvl_name_2'
asmt_claim_perf_lvl_name_3 = 'asmt_claim_perf_lvl_name_3'
score_claim_1 = 'score_claim_1'
score_claim_2 = 'score_claim_2'
score_claim_3 = 'score_claim_3'
score_claim_4 = 'score_claim_4'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
yaml_file_path = os.path.join(__location__, '..', 'datafiles', 'configs', 'datagen_config.yaml')


#@unittest.skip("skipping this test till starschema change has been made")
class Test(unittest.TestCase):

    def setUp(self):
        self.tmp_files = tempfile.mkdtemp()
        self.assertTrue(os.path.exists(self.tmp_files))
        print(self.tmp_files)

    #def tearDown(self):
        #shutil.rmtree(self.tmp_files)

    def generate_lz_data(self):
        command = 'python -m DataGeneration.src.generate_data --config DataGeneration.src.configs.dg_types_SDS --format {file} --output {dirname}'

        command = command.format(dirname=self.tmp_files, file=yaml_file_path)
        subprocess.call(command, shell=True)

    def validate_fact_asmt_csv(self):
        self.generate_lz_data()
        time.sleep(10)
        fact_asmt = glob.glob(os.path.join(self.tmp_files, 'fact_asmt_outcome.csv'))
        dim_asmt = glob.glob(os.path.join(self.tmp_files, 'dim_asmt.csv'))
        print(fact_asmt)
        print(dim_asmt)
        print(__location__)
        print(yaml_file_path)

        with open(fact_asmt[0], 'r') as new_csv:
                fact_asmt_csv = csv.DictReader(new_csv)
                for each_row in fact_asmt_csv:
                    if each_row[asmt_claim_1_score] < CLAIM_SCORE_CUT_PT1:
                        self.assertEquals(each_row[asmt_claim_1_perf_lvl], '1')
                    elif each_row[asmt_claim_1_score] < CLAIM_SCORE_CUT_PT2:
                        self.assertEquals(each_row[asmt_claim_1_perf_lvl], '2')
                    elif each_row[asmt_claim_1_score
                                  ] < CLAIM_SCORE_CUT_PT3:
                        self.assertEquals(each_row[asmt_claim_1_perf_lvl], '3')

                    if each_row[asmt_claim_2_score] < CLAIM_SCORE_CUT_PT1:
                        self.assertEquals(each_row[asmt_claim_2_perf_lvl], '1')
                    elif each_row[asmt_claim_2_score] < CLAIM_SCORE_CUT_PT2:
                        self.assertEquals(each_row[asmt_claim_2_perf_lvl], '2')
                    elif each_row[asmt_claim_2_score] < CLAIM_SCORE_CUT_PT3:
                        self.assertEquals(each_row[asmt_claim_2_perf_lvl], '3')

                    if each_row[asmt_claim_3_score] < CLAIM_SCORE_CUT_PT1:
                        self.assertEquals(each_row[asmt_claim_3_perf_lvl], '1')
                    elif each_row[asmt_claim_3_score] < CLAIM_SCORE_CUT_PT2:
                        self.assertEquals(each_row[asmt_claim_3_perf_lvl], '2')
                    elif each_row[asmt_claim_3_score] < CLAIM_SCORE_CUT_PT3:
                        self.assertEquals(each_row[asmt_claim_3_perf_lvl], '3')
        print("fact_asmt_csv varification successful")

        with open(dim_asmt[0], 'r') as dim_asmt_new:
                dim_asmt_csv = csv.DictReader(dim_asmt_new)
                for col in dim_asmt_csv:
                    self.assertEquals(col[asmt_claim_perf_lvl_name_1], 'Below Standard')
                    self.assertEquals(col[asmt_claim_perf_lvl_name_2], 'At/Near Standard')
                    self.assertEquals(col[asmt_claim_perf_lvl_name_3], 'Above Standard')
        print('dim_asmt csv varification successful')

    def validate_lzdata(self):
        lz_csv = glob.glob(os.path.join(self.tmp_files, 'realdata_asmt_id_*.csv'))
        print(lz_csv)
        with open(lz_csv[0], 'r') as new_lz_csv:
                realdata_csv = csv.DictReader(new_lz_csv)
                for each_row in realdata_csv:
                    if each_row[score_claim_1] < CLAIM_SCORE_CUT_PT1:
                        self.assertEquals(each_row[asmt_claim_1_perf_lvl], '1')
                    elif each_row[score_claim_1] < CLAIM_SCORE_CUT_PT2:
                        self.assertEquals(each_row[asmt_claim_1_perf_lvl], '2')
                    elif each_row[score_claim_1
                                  ] < CLAIM_SCORE_CUT_PT3:
                        self.assertEquals(each_row[asmt_claim_1_perf_lvl], '3')

                    if each_row[score_claim_2] < CLAIM_SCORE_CUT_PT1:
                        self.assertEquals(each_row[asmt_claim_2_perf_lvl], '1')
                    elif each_row[score_claim_2] < CLAIM_SCORE_CUT_PT2:
                        self.assertEquals(each_row[asmt_claim_2_perf_lvl], '2')
                    elif each_row[score_claim_2] < CLAIM_SCORE_CUT_PT3:
                        self.assertEquals(each_row[asmt_claim_2_perf_lvl], '3')

                    if each_row[score_claim_3] < CLAIM_SCORE_CUT_PT1:
                        self.assertEquals(each_row[asmt_claim_3_perf_lvl], '1')
                    elif each_row[score_claim_3] < CLAIM_SCORE_CUT_PT2:
                        self.assertEquals(each_row[asmt_claim_3_perf_lvl], '2')
                    elif each_row[score_claim_3] < CLAIM_SCORE_CUT_PT3:
                        self.assertEquals(each_row[asmt_claim_3_perf_lvl], '3')

    def test_validate_data(self):
        self.validate_fact_asmt_csv()
        self.validate_lzdata()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
