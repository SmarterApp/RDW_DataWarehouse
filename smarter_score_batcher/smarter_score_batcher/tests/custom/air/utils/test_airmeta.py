# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

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
