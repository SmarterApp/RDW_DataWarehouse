'''
Created on Feb 12, 2013

@author: swimberly
'''
from random import randint
import idgen
import unittest


class TestIdGen(unittest.TestCase):

    def test_IdGen(self):
        igen = idgen.IdGen()
        next_id = igen.next_id
        self.assertEqual(next_id, igen.get_id())

        for i in range(20):
            next_id += 1
            self.assertEqual(next_id, igen.get_id())

        for i in range(20):
            next_id += 1
            igen2 = idgen.IdGen()
            self.assertEqual(next_id, igen2.get_id())

        igen.set_start(5000)
        self.assertEqual(5000, igen.get_id())
        igen.set_start(1)
        self.assertEqual(1, igen.get_id())
        igen.set_start(2)
        self.assertEqual(2, igen.get_id())
        igen.set_start(1000000)
        self.assertEqual(1000000, igen.get_id())

        for i in range(30):
            next_id = randint(0, 50000)
            igen.set_start(next_id)
            self.assertEqual(next_id, igen.get_id())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
