'''
Created on Apr 28, 2013

@author: ken
'''
import unittest
import DataGeneration.src.calc.adjust as adjust


class Test(unittest.TestCase):

    # # give some idea of ranking for percentages
    # # if after adjust_pld rank got bigger for +ve adjustment, then it worked
    def rank(self, pcs):
        mult = 1
        myrank = 0
        for x in pcs:
            myrank += mult * x
            mult *= 2
        return myrank

    def doit(self, pci, adjustment):
        pco = adjust.adjust_pld(pci, adjustment)
        oldsum = sum(pci)
        newsum = sum(pco)
        oldrank = self.rank(pci)
        newrank = self.rank(pco)
        print()
        if adjustment > 0:
            print("adjust up by " + str(int(adjustment * 100)) + "%  rank ", newrank, ">", oldrank)
        else:
            print("adjust down by " + str(int(adjustment * 100)) + "%  rank ", newrank, "<", oldrank)
        print("OLD=", str(pci), oldsum)
        print("NEW=", str(pco), newsum)
        return oldrank, newrank

    def test_adust01(self):
        adjustment = 0.5
        pci = [30, 34, 28, 9]
        oldrank, newrank = self.doit(pci, adjustment)
        if adjustment > 0:
            assert(newrank > oldrank)
        else:
            assert(newrank < oldrank)

    def test_adust02(self):
        adjustment = -0.7
        pci = [30, 34, 28, 9]
        oldrank, newrank = self.doit(pci, adjustment)
        if adjustment > 0:
            assert(newrank > oldrank)
        else:
            assert(newrank < oldrank)

    def test_adust03(self):
        adjustment = 0.5
        pci = [21, 44, 32, 3]
        oldrank, newrank = self.doit(pci, adjustment)
        if adjustment > 0:
            assert(newrank > oldrank)
        else:
            assert(newrank < oldrank)

    def test_adust04(self):
        adjustment = -0.7
        pci = [21, 44, 32, 3]
        oldrank, newrank = self.doit(pci, adjustment)
        if adjustment > 0:
            assert(newrank > oldrank)
        else:
            assert(newrank < oldrank)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_adust01']
    unittest.main()
