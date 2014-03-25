__author__ = 'npandey'
"""
Test Student Registration State Visitor
"""

from sqlalchemy.sql.expression import select

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (Unittest_with_edcore_sqlite, UnittestEdcoreDBConnection,
                                                            get_unittest_tenant_name)
#from edextract.tasks.student_reg_constants import TableName
#import edextract.data_extract_generation.sr_state_visitor as sr_state_visitor


class TestSRStateVisitor(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        with UnittestEdcoreDBConnection() as connection:
            student_reg = connection.get_table('student_reg')
            query = select([student_reg.c.state_name, student_reg.c.district_name, student_reg.c.school_name], from_obj=[student_reg])

        self.results = connection.get_streaming_result(query)

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

#    def test_visit(self):
#        for row in self.results:
#            sr_state_visitor.visit(row)

