'''
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from sqlalchemy.sql.expression import select, and_
from smarter.trigger.pre_pdf_generator import update_ed_stats_for_prepdf
from edcore.database.stats_connector import StatsDBConnection


class Test(Unittest_with_stats_sqlite):

    def testUpdate_ed_stats_for_pre_pdf(self):
        update_ed_stats_for_prepdf('9000')
        with StatsDBConnection() as connector:
            udl_stats = connector.get_table('udl_stats')
            query = select([udl_stats.c.last_pdf_task_requested.label('last_pdf_task_requested'), ],
                           from_obj=[udl_stats])
            query = query.where(and_(udl_stats.c.rec_id == '9000'))
            results = connector.get_result(query)
        self.assertIsNotNone(results[0]['last_pdf_task_requested'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
