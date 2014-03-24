import os
import unittest
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.database.udl2_connector import initialize_db_target,\
    initialize_db_udl, initialize_db_prod, get_target_connection,\
    get_udl_connection


class UDLTestHelper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE

        conf_tup = read_ini_file(config_path)
        cls.udl2_conf = conf_tup[0]
        initialize_db_udl(cls.udl2_conf)
        initialize_db_target(cls.udl2_conf)
        initialize_db_prod(cls.udl2_conf)
        cls.truncate_edware_tables()
        cls.truncate_udl_tables()

    @classmethod
    def tearDownClass(cls):
        cls.truncate_edware_tables()
        cls.truncate_udl_tables()

    @classmethod
    def truncate_edware_tables(self):
        with get_target_connection(schema_name=self.udl2_conf['target_db']['db_schema']) as conn:
            metadata = conn.get_metadata()
            for table in reversed(metadata.sorted_tables):
                conn.execute(table.delete())

    @classmethod
    def truncate_udl_tables(self):
        tables = ['INT_SBAC_ASMT', 'INT_SBAC_ASMT_OUTCOME', 'STG_SBAC_ASMT_OUTCOME', 'ERR_LIST']
        with get_udl_connection() as conn:
            for t in tables:
                table = conn.get_table(t)
                conn.execute(table.delete())

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
        with get_udl_connection() as conn:
            result = conn.execute(stg_avg_query)
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
        with get_udl_connection() as conn:
            result = conn.execute(query)
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
        with get_target_connection() as conn:
            result = conn.execute(star_avg_query)
        for row in result:
            star_asmt_avgs = row

        return star_asmt_avgs

    def get_staging_demographic_counts(self):
        demographics = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1']
        results_dict = {}
        with get_udl_connection() as conn:
            for entry in demographics:
                #get staging
                demo_query = """ select count({demographic}) from "udl2"."STG_SBAC_ASMT_OUTCOME" where {demographic} = 'Y' or {demographic} = 'y' or {demographic} = 'yes';""".format(demographic=entry)
                result = conn.execute(demo_query)
                for row in result:
                    demo_count = row[0]

                results_dict[entry] = demo_count

        return results_dict

    def get_integration_demographic_counts(self):
        demographics = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1']
        results_dict = {}
        with get_udl_connection() as conn:
            for entry in demographics:
                #get staging
                demo_query = """ select count({demographic}) from "udl2"."INT_SBAC_ASMT_OUTCOME" where {demographic};""".format(demographic=entry)
                result = conn.execute(demo_query)
                for row in result:
                    demo_count = row[0]

                results_dict[entry] = demo_count

            #get derived ethnicity
            eth_query = """ select count({demographic}) from "udl2"."INT_SBAC_ASMT_OUTCOME" where {demographic} IS NOT NULL;""".format(demographic='dmg_eth_derived')
            result = conn.execute(eth_query)
            for row in result:
                derived_count = row[0]
            results_dict['dmg_eth_derived'] = derived_count

        return results_dict

    def get_star_schema_demographic_counts(self):
        demographics = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1']
        results_dict = {}
        with get_target_connection() as conn:
            for entry in demographics:
                #get staging
                demo_query = """ select count({demographic}) from "edware"."fact_asmt_outcome" where {demographic};""".format(demographic=entry)
                result = conn.execute(demo_query)
                for row in result:
                    demo_count = row[0]

                results_dict[entry] = demo_count

                #get derived ethnicity
                eth_query = """ select count({demographic}) from "edware"."fact_asmt_outcome" where {demographic} IS NOT NULL;""".format(demographic='dmg_eth_derived')
                result = conn.execute(eth_query)
                for row in result:
                    derived_count = row[0]
                results_dict['dmg_eth_derived'] = derived_count

        return results_dict
