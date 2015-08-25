'''
Created on Jun 12, 2015

@author: tosako
'''
import unittest
from smarter_score_batcher.custom.air.utils.air_meta import AIRMeta,\
    TSBAIRUnknownAsmtTypeException


class Test(unittest.TestCase):

    def testAirMeta(self):
        airMeta = AIRMeta(True, 'student_id', 'state_code', 'district_id', 'academic_year', 'summative', 'subject', 'grade', 'effective_date', 'SBAC-ICA-FIXED-G3E-COMBINED')
        self.assertEqual("SUMMATIVE", airMeta.asmt_type)
        airMeta = AIRMeta(True, 'student_id', 'state_code', 'district_id', 'academic_year', 'interim', 'subject', 'grade', 'effective_date', 'SBAC-ICA-FIXED-G3E-COMBINED')
        self.assertEqual("INTERIM COMPREHENSIVE", airMeta.asmt_type)
        airMeta = AIRMeta(True, 'student_id', 'state_code', 'district_id', 'academic_year', 'interim', 'subject', 'grade', 'effective_date', 'SBAC-ICA-FIXED-G3E-COMBINED')
        self.assertEqual("INTERIM COMPREHENSIVE", airMeta.asmt_type)
        airMeta = AIRMeta(True, 'student_id', 'state_code', 'district_id', 'academic_year', 'interim', 'subject', 'grade', 'effective_date', 'SBAC-IAB-FIXED-G11E-ListenInterpet-ELA-11')
        self.assertEqual("INTERIM ASSESSMENT BLOCKS", airMeta.asmt_type)
        airMeta = AIRMeta(True, 'student_id', 'state_code', 'district_id', 'academic_year', 'interim', 'subject', 'grade', 'effective_date', 'SBAC-iAb-FIXED-G11E-ListenInterpet-ELA-11')
        self.assertEqual("INTERIM ASSESSMENT BLOCKS", airMeta.asmt_type)
        try:
            '''
            use try-exception, assertRaises does not work.
            '''
            airMeta = AIRMeta(True, 'student_id', 'state_code', 'district_id', 'academic_year', 'interim', 'subject', 'grade', 'effective_date', 'unknown asmt_id')
            self.fail('should raise exception before')
        except TSBAIRUnknownAsmtTypeException:
            pass
        except:
            self.fail('unexpected exception before')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
