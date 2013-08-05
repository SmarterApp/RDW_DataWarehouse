import os
import imp
from udl2 import database
from udl2_util.database_util import execute_queries
import unittest
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE


class UDLTestHelper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        cls.udl2_conf = udl2_conf
        cls.udl2_conn, cls.udl2_engine = database._create_conn_engine(cls.udl2_conf['udl2_db'])
        cls.target_conn, cls.target_engine = database._create_conn_engine(cls.udl2_conf['target_db'])

    @classmethod
    def tearDownClass(cls):
        cls.udl2_conn.close()
        cls.target_conn.close()

    def setUp(self):
        self.truncate_edware_tables()
        self.truncate_udl_tables()

    def tearDown(self):
        print('here6')
        #self.truncate_edware_tables()
        print('here7')
        #self.truncate_udl_tables()
        print('here8')

    def truncate_edware_tables(self):
        template = """
            TRUNCATE "{target_schema}"."{target_table}" CASCADE
            """

        sql_dim_asmt = template.format(target_schema=self.udl2_conf['target_db']['db_schema'], target_table='dim_asmt')
        sql_dim_inst_hier = template.format(target_schema=self.udl2_conf['target_db']['db_schema'], target_table='dim_inst_hier')
        sql_dim_section = template.format(target_schema=self.udl2_conf['target_db']['db_schema'], target_table='dim_section')
        sql_dim_staff = template.format(target_schema=self.udl2_conf['target_db']['db_schema'], target_table='dim_staff')
        sql_dim_student = template.format(target_schema=self.udl2_conf['target_db']['db_schema'], target_table='dim_student')
        sql_fact_asmt_outcome = template.format(target_schema=self.udl2_conf['target_db']['db_schema'], target_table='fact_asmt_outcome')
        except_msg = "Unable to clean up target db tabels"
        execute_queries(self.target_conn, [sql_dim_asmt, sql_dim_inst_hier, sql_dim_section, sql_dim_staff, sql_dim_student, sql_fact_asmt_outcome], except_msg)

    def truncate_udl_tables(self):
        print('abc')
        sql_template = """
            TRUNCATE "{staging_schema}"."{staging_table}" CASCADE
            """
        sql_int_asmt = sql_template.format(staging_schema=self.udl2_conf['udl2_db']['integration_schema'],
                                           staging_table='INT_SBAC_ASMT')
        sql_int_asmt_outcome = sql_template.format(staging_schema=self.udl2_conf['udl2_db']['integration_schema'],
                                                   staging_table='INT_SBAC_ASMT_OUTCOME')

        sql_stg_asmt = sql_template.format(staging_schema=self.udl2_conf['udl2_db']['integration_schema'],
                                           staging_table='STG_SBAC_ASMT')
        sql_stg_asmt_outcome = sql_template.format(staging_schema=self.udl2_conf['udl2_db']['integration_schema'],
                                                   staging_table='STG_SBAC_ASMT_OUTCOME')

        except_msg = "Unable to clean up udl tables"
        execute_queries(self.udl2_conn, [sql_int_asmt, sql_int_asmt_outcome, sql_stg_asmt, sql_stg_asmt_outcome], except_msg)
        print('def')

    def get_staging_asmt_score_avgs(self):
        stg_avg_query = """ select avg(score_asmt::int),
        avg(score_asmt_min::int),
        avg(score_asmt_max::int),
        avg(score_claim_1::int),
        avg(score_claim_1_min::int),
        avg(score_claim_1_max::int),
        avg(score_claim_2::int),
        avg(score_claim_2_min::int),
        avg(score_claim_2_max::int),
        avg(score_claim_3::int),
        avg(score_claim_3_min::int),
        avg(score_claim_3_max::int),
        avg(score_claim_4::int),
        avg(score_claim_4_min::int),
        avg(score_claim_4_max::int) from "udl2"."STG_SBAC_ASMT_OUTCOME" """

        result = self.udl2_conn.execute(stg_avg_query)
        for row in result:
            asmt_avgs = row

        return asmt_avgs

    def get_integration_asmt_score_avgs(self):
        query = """ SELECT avg(score_asmt),
        avg(score_asmt_min),
        avg(score_asmt_max),
        avg(score_claim_1),
        avg(score_claim_1_min),
        avg(score_claim_1_max),
        avg(score_claim_2),
        avg(score_claim_2_min),
        avg(score_claim_2_max),
        avg(score_claim_3),
        avg(score_claim_3_min),
        avg(score_claim_3_max),
        avg(score_claim_4),
        avg(score_claim_4_min),
        avg(score_claim_4_max) FROM udl2."INT_SBAC_ASMT_OUTCOME" """

        result = self.udl2_conn.execute(query)
        for row in result:
            asmt_avgs = row

        return asmt_avgs

    def get_edware_asmt_score_avgs(self):
        star_avg_query = """ select avg(asmt_score),
        avg(asmt_score_range_min),
        avg(asmt_score_range_max),
        avg(asmt_claim_1_score),
        avg(asmt_claim_1_score_range_min),
        avg(asmt_claim_1_score_range_max),
        avg(asmt_claim_2_score),
        avg(asmt_claim_2_score_range_min),
        avg(asmt_claim_2_score_range_max),
        avg(asmt_claim_3_score),
        avg(asmt_claim_3_score_range_min),
        avg(asmt_claim_3_score_range_max),
        avg(asmt_claim_4_score),
        avg(asmt_claim_4_score_range_min),
        avg(asmt_claim_4_score_range_max) from edware.fact_asmt_outcome """
        result = self.target_conn.execute(star_avg_query)
        for row in result:
            star_asmt_avgs = row

        return star_asmt_avgs

    def get_staging_demographic_counts(self):
        demographics = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1']
        results_dict = {}

        for entry in demographics:
            #get staging
            demo_query = """ select count({demographic}) from "udl2"."STG_SBAC_ASMT_OUTCOME" where {demographic} = 'Y' or {demographic} = 'y' or {demographic} = 'yes';""".format(demographic=entry)
            result = self.udl2_conn.execute(demo_query)
            for row in result:
                demo_count = row[0]

            results_dict[entry] = demo_count

        return results_dict

    def get_integration_demographic_counts(self):
        demographics = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1']
        results_dict = {}

        for entry in demographics:
            #get staging
            demo_query = """ select count({demographic}) from "udl2"."INT_SBAC_ASMT_OUTCOME" where {demographic};""".format(demographic=entry)
            result = self.udl2_conn.execute(demo_query)
            for row in result:
                demo_count = row[0]

            results_dict[entry] = demo_count

        return results_dict