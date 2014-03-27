'''
Created on Mar 26, 2014

@author: tosako
'''
import unittest
from edmigrate.utils.conductor import Conductor
from edmigrate.exceptions import ConductorTimeoutException


class Test(unittest.TestCase):

    def test_conductor_lock(self):
        conductor1 = Conductor()
        self.assertRaises(ConductorTimeoutException, Conductor, locktimeout=1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_conductor_lock']
    unittest.main()
