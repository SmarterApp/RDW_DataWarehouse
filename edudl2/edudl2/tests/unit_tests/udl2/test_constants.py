import unittest
from edudl2.udl2.constants import Constants

__author__ = 'sravi'


class TestConstants(unittest.TestCase):

    def test_all_udl_constants(self):
        self.assertEqual(Constants.SR_TARGET_TABLE, 'student_reg')

        # staging tables
        self.assertEqual(Constants.STG_ASMT_OUT_TABLE, 'stg_sbac_asmt_outcome')
        self.assertEqual(Constants.STG_SR_TABLE, 'stg_sbac_stu_reg')

        # integration tables
        self.assertEqual(Constants.INT_ASMT_TABLE, 'int_sbac_asmt')
        self.assertEqual(Constants.INT_ASMT_OUT_TABLE, 'int_sbac_asmt_outcome')
        self.assertEqual(Constants.INT_SR_META_TABLE, 'int_sbac_stu_reg_meta')
        self.assertEqual(Constants.INT_SR_TABLE, 'int_sbac_stu_reg')

        # other tables
        self.assertEqual(Constants.UDL2_BATCH_TABLE, 'udl_batch')
        self.assertEqual(Constants.ASMT_REF_TABLE, 'ref_column_mapping')
        self.assertEqual(Constants.SR_REF_TABLE, 'sr_ref_column_mapping')
        self.assertEqual(Constants.UDL2_ERR_LIST_TABLE, 'err_list')
        self.assertEqual(Constants.UDL2_CSV_LZ_TABLE, 'lz_csv')
        self.assertEqual(Constants.UDL2_JSON_LZ_TABLE, 'lz_json')
        self.assertEqual(Constants.UDL2_FDW_SERVER, 'udl2_fdw_server')

        # column values
        self.assertEqual(Constants.OP_COLUMN_NAME, 'op')

        # load types
        self.assertEqual(Constants.LOAD_TYPE_KEY, 'Content')
        self.assertEqual(Constants.LOAD_TYPE_ASSESSMENT, 'assessment')
        self.assertEqual(Constants.LOAD_TYPE_STUDENT_REGISTRATION, 'studentregistration')

        # assessment types
        self.assertEqual(Constants.ASSESSMENT_TYPE_KEY, 'Identification.Type')
        self.assertEqual(Constants.ASSESSMENT_TYPE_SUMMATIVE, 'SUMMATIVE')
        self.assertEqual(Constants.ASSESSMENT_TYPE_INTERIM_COMPREHENSIVE, 'INTERIM COMPREHENSIVE')
        self.assertEqual(Constants.ASSESSMENT_TYPE_INTERIM_ASSESSMENT_BLOCKS, 'INTERIM ASSESSMENT BLOCKS')

        self.assertEqual(Constants.SEQUENCE_NAME, 'global_rec_seq')

    def test_all_lambda_constants(self):
        self.assertEqual(len(Constants.LOAD_TYPES()), 2)
        self.assertEqual(Constants.LOAD_TYPES(), [Constants.LOAD_TYPE_ASSESSMENT, Constants.LOAD_TYPE_STUDENT_REGISTRATION])
        self.assertEqual(len(Constants.ASSESSMENT_TYPES()), 3)
        self.assertEqual(Constants.ASSESSMENT_TYPES(), [Constants.ASSESSMENT_TYPE_SUMMATIVE, Constants.ASSESSMENT_TYPE_INTERIM_COMPREHENSIVE, Constants.ASSESSMENT_TYPE_INTERIM_ASSESSMENT_BLOCKS])
        self.assertEqual(Constants.UDL2_STAGING_TABLE(Constants.LOAD_TYPE_ASSESSMENT), Constants.STG_ASMT_OUT_TABLE)
        self.assertEqual(Constants.UDL2_STAGING_TABLE(Constants.LOAD_TYPE_STUDENT_REGISTRATION), Constants.STG_SR_TABLE)
        self.assertEqual(Constants.UDL2_INTEGRATION_TABLE(Constants.LOAD_TYPE_ASSESSMENT), Constants.INT_ASMT_OUT_TABLE)
        self.assertEqual(Constants.UDL2_INTEGRATION_TABLE(Constants.LOAD_TYPE_STUDENT_REGISTRATION), Constants.INT_SR_TABLE)
        self.assertEqual(Constants.UDL2_JSON_INTEGRATION_TABLE(Constants.LOAD_TYPE_ASSESSMENT), Constants.INT_ASMT_TABLE)
        self.assertEqual(Constants.UDL2_JSON_INTEGRATION_TABLE(Constants.LOAD_TYPE_STUDENT_REGISTRATION), Constants.INT_SR_META_TABLE)
        self.assertEqual(Constants.UDL2_REF_MAPPING_TABLE(Constants.LOAD_TYPE_ASSESSMENT), Constants.ASMT_REF_TABLE)
        self.assertEqual(Constants.UDL2_REF_MAPPING_TABLE(Constants.LOAD_TYPE_STUDENT_REGISTRATION), Constants.SR_REF_TABLE)
        self.assertEqual(Constants.TENANT_SEQUENCE_NAME('cat'), Constants.SEQUENCE_NAME + '_' + 'cat')
        self.assertEqual(Constants.TENANT_SEQUENCE_NAME(''), None)
        self.assertEqual(Constants.TENANT_SEQUENCE_NAME(None), None)
