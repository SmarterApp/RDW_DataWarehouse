import unittest
import util_2 as util
import re
import datetime


class TestUtil2(unittest.TestCase):

    def test_generate_email_address(self):
        email = util.generate_email_address('John', 'Doe', 'test')
        self.assertIsNotNone(re.match("[^@]+@[^@]+\.[^@]+", email))

    def test_generate_address(self):
        streets = ['Main', 'Park', 'Front']
        address = util.generate_address(streets)
        self.assertIsNotNone(re.match("\d+ [A-Za-z]+ [A-Za-z]+", address))

    def test_generate_dob(self):
        grade = 4
        dob = util.generate_dob(grade)
        # self.assertIsInstance(dob, date)
        aprox_age = grade + 6
        birth_year = datetime.date.today().year - aprox_age
        self.assertEqual(dob[0:4], str(birth_year))
