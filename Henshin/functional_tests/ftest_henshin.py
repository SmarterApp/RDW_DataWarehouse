'''
Created on Mar 29, 2013

@author: swimberly
'''

import os
import re
import src.henshin as henshin


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def ftest_henshin():
    dim_asmt = os.path.join(__location__, 'data', 'dim_asmt_for_test.csv')
    fact_outcome = os.path.join(__location__, 'data', 'valid_fact_asmt_outcome.csv')
    output_path = os.path.join(__location__, 'data', 'henshin_files')
    henshin.henshin(dim_asmt, fact_outcome, output_path)

    output_json = [f for f in os.listdir(output_path) if re.match(r'(?P<name>.*\.json)', f)]
    output_csv = [f for f in os.listdir(output_path) if re.match(r'(?P<name>.*\.csv)', f)]
