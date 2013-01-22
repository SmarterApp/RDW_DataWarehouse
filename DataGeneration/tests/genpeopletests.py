'''
Created on Jan 16, 2013

@author: swimberly
'''
import unittest
import genpeople
from objects.nameinfo import NameInfo


class Test(unittest.TestCase):

    def test_generate_people(self):
        result = genpeople.generate_people(genpeople.STUDENT, 10, 0.5)

        self.assertEqual(len(result), 10)
        male_count = 0
        for p in result:
            if p.gender == 'male':
                male_count += 1

        self.assertEqual(male_count, 5)

#    def test_generate_student(self):
#        self.assertIsNone(genpeople.generate_student(0, 0, [], [], []))
#
#        bob = NameInfo('bob', 1, 1, 1)
#        ann = NameInfo('ann', 1, 1, 1)
#        smith = NameInfo('smith', 1, 1, 1)
#
#        result = genpeople.generate_student(10, 0.5, [bob], [ann], [smith])
#
#        self.assertEqual(len(result), 10)
#        anncount = 0
#        bobcount = 0
#
#        for student in result:
#            self.assertEqual(student.lastname, 'smith')
#            if student.firstname == 'bob':
#                bobcount += 1
#            elif student.firstname == 'ann':
#                anncount += 1
#
#        self.assertEqual(bobcount, 5)
#        self.assertEqual(anncount, 5)
#
#        # check for ratio greater than 1, define behavior for
#        # situation

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
