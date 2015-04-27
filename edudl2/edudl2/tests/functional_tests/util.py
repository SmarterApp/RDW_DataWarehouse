from edudl2.database.udl2_connector import initialize_db_target,\
    initialize_db_udl, initialize_db_prod, get_target_connection,\
    get_udl_connection
from sqlalchemy.sql.expression import select, func, true, cast
from sqlalchemy.types import Integer
from edcore.database.utils.utils import create_schema, drop_schema
from edschema.metadata.ed_metadata import generate_ed_metadata
from edschema.metadata.util import get_tables_starting_with
from edudl2.tests.functional_tests import UDLFunctionalTestCase


class UDLTestHelper(UDLFunctionalTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.truncate_udl_tables()

    @classmethod
    def tearDownClass(cls):
        cls.truncate_udl_tables()

    @classmethod
    def truncate_edware_tables(self, schema, tenant='cat'):
        with get_target_connection(tenant, schema_name=schema) as conn:
            metadata = conn.get_metadata()
            for table in reversed(metadata.sorted_tables):
                conn.execute(table.delete())

    @classmethod
    def truncate_udl_tables(self):
        with get_udl_connection() as conn:
            tables = get_tables_starting_with(conn.get_metadata(), 'int_') + \
                get_tables_starting_with(conn.get_metadata(), 'stg_') + ['err_list', 'udl_batch']
            for t in tables:
                table = conn.get_table(t)
                conn.execute(table.delete())

    @classmethod
    def create_schema_for_target(cls, tenant, guid_batch):
        with get_target_connection(tenant) as connector:
            create_schema(connector, generate_ed_metadata, guid_batch)

    @classmethod
    def drop_target_schema(cls, tenant, guid_batch):
        with get_target_connection(tenant) as connector:
            drop_schema(connector, guid_batch)

    def get_staging_asmt_score_avgs(self):
        with get_udl_connection() as conn:
            stg_outcome = conn.get_table('stg_sbac_asmt_outcome')
            query = select([func.avg(cast(stg_outcome.c.assessmentsubtestresultscorevalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestminimumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestmaximumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestresultscoreclaim1value, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestclaim1minimumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestclaim1maximumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestresultscoreclaim2value, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestclaim2minimumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestclaim2maximumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestresultscoreclaim3value, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestclaim3minimumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestclaim3maximumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestresultscoreclaim4value, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestclaim4minimumvalue, Integer)),
                            func.avg(cast(stg_outcome.c.assessmentsubtestclaim4maximumvalue, Integer))], from_obj=stg_outcome)
            result = conn.execute(query)
            for row in result:
                asmt_avgs = row

            return asmt_avgs

    def get_integration_asmt_score_avgs(self):
        with get_udl_connection() as conn:
            int_outcome = conn.get_table('int_sbac_asmt_outcome')
            query = select([func.avg(int_outcome.c.score_asmt),
                            func.avg(int_outcome.c.score_asmt_min),
                            func.avg(int_outcome.c.score_asmt_max),
                            func.avg(int_outcome.c.score_claim_1),
                            func.avg(int_outcome.c.score_claim_1_min),
                            func.avg(int_outcome.c.score_claim_1_max),
                            func.avg(int_outcome.c.score_claim_2),
                            func.avg(int_outcome.c.score_claim_2_min),
                            func.avg(int_outcome.c.score_claim_2_max),
                            func.avg(int_outcome.c.score_claim_3),
                            func.avg(int_outcome.c.score_claim_3_min),
                            func.avg(int_outcome.c.score_claim_3_max),
                            func.avg(int_outcome.c.score_claim_4),
                            func.avg(int_outcome.c.score_claim_4_min),
                            func.avg(int_outcome.c.score_claim_4_max)], from_obj=int_outcome)
            result = conn.execute(query)
            for row in result:
                asmt_avgs = row

            return asmt_avgs

    def get_edware_asmt_score_avgs(self, tenant, schema):
        with get_target_connection(tenant, schema) as conn:
            fact = conn.get_table('fact_asmt_outcome_vw')
            query = select([func.avg(fact.c.asmt_score),
                            func.avg(fact.c.asmt_score_range_min),
                            func.avg(fact.c.asmt_score_range_max),
                            func.avg(fact.c.asmt_claim_1_score),
                            func.avg(fact.c.asmt_claim_1_score_range_min),
                            func.avg(fact.c.asmt_claim_1_score_range_max),
                            func.avg(fact.c.asmt_claim_2_score),
                            func.avg(fact.c.asmt_claim_2_score_range_min),
                            func.avg(fact.c.asmt_claim_2_score_range_max),
                            func.avg(fact.c.asmt_claim_3_score),
                            func.avg(fact.c.asmt_claim_3_score_range_min),
                            func.avg(fact.c.asmt_claim_3_score_range_max),
                            func.avg(fact.c.asmt_claim_4_score),
                            func.avg(fact.c.asmt_claim_4_score_range_min),
                            func.avg(fact.c.asmt_claim_4_score_range_max)], from_obj=fact)
            result = conn.execute(query)
            for row in result:
                star_asmt_avgs = row

            return star_asmt_avgs

    def get_staging_demographic_counts(self):
        demographics = ['hispanicorlatinoethnicity', 'americanindianoralaskanative', 'asian', 'blackorafricanamerican',
                        'nativehawaiianorotherpacificislander', 'white', 'demographicracetwoormoreraces',
                        'ideaindicator', 'lepstatus', 'section504status', 'economicdisadvantagestatus',
                        'migrantstatus']
        results_dict = {}
        with get_udl_connection() as conn:
            stg_outcome = conn.get_table('stg_sbac_asmt_outcome')
            for entry in demographics:
                query = select([func.count(stg_outcome.c[entry])], from_obj=stg_outcome).where(stg_outcome.c[entry].in_(['Y', 'y', 'yes']))
                result = conn.execute(query)
                for row in result:
                    demo_count = row[0]

                results_dict[entry] = demo_count

        corrleated_results = {
            'dmg_eth_hsp': results_dict['hispanicorlatinoethnicity'],
            'dmg_eth_ami': results_dict['americanindianoralaskanative'],
            'dmg_eth_asn': results_dict['asian'],
            'dmg_eth_blk': results_dict['blackorafricanamerican'],
            'dmg_eth_pcf': results_dict['nativehawaiianorotherpacificislander'],
            'dmg_eth_wht': results_dict['white'],
            'dmg_eth_2om': results_dict['demographicracetwoormoreraces'],
            'dmg_prg_iep': results_dict['ideaindicator'],
            'dmg_prg_lep': results_dict['lepstatus'],
            'dmg_prg_504': results_dict['section504status'],
            'dmg_sts_ecd': results_dict['economicdisadvantagestatus'],
            'dmg_sts_mig': results_dict['migrantstatus'],
        }

        return corrleated_results

    def get_integration_demographic_counts(self):
        demographics = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht',
                        'dmg_eth_2om', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_sts_ecd', 'dmg_sts_mig']
        results_dict = {}
        with get_udl_connection() as conn:
            int_outcome = conn.get_table('int_sbac_asmt_outcome')
            for entry in demographics:
                query = select([func.count(int_outcome.c[entry])], from_obj=int_outcome).where(int_outcome.c[entry] == true())
                result = conn.execute(query)
                for row in result:
                    demo_count = row[0]

                results_dict[entry] = demo_count

            #get derived ethnicity
            eth_query = select([func.count(int_outcome.c[entry])], from_obj=int_outcome).where(int_outcome.c[entry] is not None)
            result = conn.execute(eth_query)
            for row in result:
                derived_count = row[0]
            results_dict['dmg_eth_derived'] = derived_count

        return results_dict

    def get_star_schema_demographic_counts(self, tenant, schema):
        demographics = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_eth_2om',
                        'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_sts_ecd', 'dmg_sts_mig']
        results_dict = {}
        with get_target_connection(tenant, schema) as conn:
            fact = conn.get_table('fact_asmt_outcome_vw')
            for entry in demographics:
                demo_query = select([func.count(fact.c[entry])], from_obj=fact).where(fact.c[entry] == true())
                result = conn.execute(demo_query)
                for row in result:
                    demo_count = row[0]

                results_dict[entry] = demo_count

                #get derived ethnicity
                eth_query = select([func.count(fact.c.dmg_eth_derived)], from_obj=fact).where(fact.c.dmg_eth_derived is not None)
                result = conn.execute(eth_query)
                for row in result:
                    derived_count = row[0]
                results_dict['dmg_eth_derived'] = derived_count

        return results_dict
