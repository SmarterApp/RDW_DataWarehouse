'''
Created on Jul 29, 2013

@author: swimberly
'''
import unittest
import os
import csv
from demographics import Demographics, DemographicStatus

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Test(unittest.TestCase):

    def setUp(self):
        self.dem_obj = Demographics(write_test_csv_file())
        self.dem_id = 'typical1'

    def tearDown(self):
        pass

    def test_get_demo_names(self):
        result = self.dem_obj.get_demo_names(self.dem_id, 'math', 3)


class DummyClass(object):
    pass


def write_test_csv_file():
    csv_file_data = [
        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '3', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '3', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '3', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '3', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '3', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '3', 'Hispanic or Latino', 'dmg_eth_his', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '3', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '3', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '3', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '3', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '3', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '12', 'All Students', 'all', '100', '7', '32', '41', '20'),
        ('typical1', '1', 'math', '12', 'Female', 'female', '49', '6', '31', '43', '20'),
        ('typical1', '1', 'math', '12', 'Male', 'male', '51', '8', '33', '40', '19'),
        ('typical1', '2', 'math', '12', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '9', '40', '39', '12'),
        ('typical1', '2', 'math', '12', 'Black or African American', 'dmg_eth_blk', '19', '14', '45', '34', '7'),
        ('typical1', '2', 'math', '12', 'Hispanic or Latino', 'dmg_eth_his', '22', '11', '40', '39', '10'),
        ('typical1', '2', 'math', '12', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '8', '2', '14', '37', '47'),
        ('typical1', '2', 'math', '12', 'White', 'dmg_eth_wht', '50', '4', '25', '47', '24'),
        ('typical1', '3', 'math', '12', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '16', '27', '50', '21', '2'),
        ('typical1', '4', 'math', '12', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '12', 'Economically Disadvantaged', 'dmg_prg_tt1', '56', '20', '38', '39', '3')
    ]

    file_path = os.path.join(__location__, 'test_file.csv')

    with open(file_path, 'w') as cfile:
        cwriter = csv.writer(cfile)
        for row in csv_file_data:
            cwriter.writerow(row)

    return file_path


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()