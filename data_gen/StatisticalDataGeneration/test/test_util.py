import unittest
from util import generate_email_address, generate_address, generate_dob
import re
from datetime import datetime, date


class TestUtil(unittest.TestCase):

    def test_generate_email_address(self):
        email = generate_email_address('John', 'Doe', 'test')
        self.assertIsNotNone(re.match("[^@]+@[^@]+\.[^@]+", email))

    def test_generate_address(self):
        streets = ['Main', 'Park', 'Front']
        address = generate_address(streets)
        self.assertIsNotNone(re.match("\d+ [A-Za-z]+ [A-Za-z]+", address))

    def test_generate_dob(self):
        grade = 4
        dob = generate_dob(grade)
        # self.assertIsInstance(dob, date)
        aprox_age = grade + 6
        birth_year = datetime.now().year - aprox_age
        self.assertEqual(dob[0:4], str(birth_year))


if __name__ == "__main__":
    unittest.main()
