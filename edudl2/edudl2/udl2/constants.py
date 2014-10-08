from edcore.database.utils.constants import LoadType
from edcore.database.utils.constants import AssessmentType
__author__ = 'sravi'


class Constants():
    """
    constants related to udl db schema
    """
    UDL2_DB_CONN = 'udl2_db_conn'

    DB_SCHEMA = 'db_schema'
    URL = 'url'

    # table names
    SR_TARGET_TABLE = 'student_reg'

    # staging tables
    STG_ASMT_OUT_TABLE = 'stg_sbac_asmt_outcome'
    STG_SR_TABLE = 'stg_sbac_stu_reg'

    # integration tables
    INT_ASMT_TABLE = 'int_sbac_asmt'
    INT_ASMT_OUT_TABLE = 'int_sbac_asmt_outcome'
    INT_SR_META_TABLE = 'int_sbac_stu_reg_meta'
    INT_SR_TABLE = 'int_sbac_stu_reg'

    # other tables
    UDL2_BATCH_TABLE = 'udl_batch'
    ASMT_REF_TABLE = 'ref_column_mapping'
    SR_REF_TABLE = 'sr_ref_column_mapping'
    UDL2_ERR_LIST_TABLE = 'err_list'
    UDL2_CSV_LZ_TABLE = 'lz_csv'
    UDL2_JSON_LZ_TABLE = 'lz_json'
    UDL2_FDW_SERVER = 'udl2_fdw_server'

    # column values
    OP_COLUMN_NAME = 'op'
    GUID_ASMT = 'guid_asmt'
    STG_GUID_ASMT = 'assessmentguid'

    # load types
    LOAD_TYPE_KEY = 'content'
    LOAD_TYPE_ASSESSMENT = LoadType.ASSESSMENT
    LOAD_TYPE_STUDENT_REGISTRATION = LoadType.STUDENT_REGISTRATION

    # assessment types
    ASSESSMENT_TYPE_KEY = 'Identification.Type'
    ASSESSMENT_TYPE_SUMMATIVE = AssessmentType.SUMMATIVE
    ASSESSMENT_TYPE_INTERIM_COMPREHENSIVE = AssessmentType.INTERIM_COMPREHENSIVE
    ASSESSMENT_TYPE_INTERIM_ASSESSMENT_BLOCKS = AssessmentType.INTERIM_ASSESSMENTS_BLOCKS

    # global sequence name
    SEQUENCE_NAME = 'global_rec_seq'

    ZONES = 'zones'
    ARRIVALS = 'arrivals'

    # Phase number
    INT_TO_STAR_PHASE = 4

    # File extensions
    PROCESSING_FILE_EXT = '.processing'

    # lambdas for returning list of constants or constants based on some condition
    # TODO: in future this will be replaced with dynamic udl schema based on load being processed
    LOAD_TYPES = lambda: [Constants.LOAD_TYPE_ASSESSMENT, Constants.LOAD_TYPE_STUDENT_REGISTRATION]
    ASSESSMENT_TYPES = lambda: [Constants.ASSESSMENT_TYPE_SUMMATIVE, Constants.ASSESSMENT_TYPE_INTERIM_COMPREHENSIVE, Constants.ASSESSMENT_TYPE_INTERIM_ASSESSMENT_BLOCKS]
    UDL2_STAGING_TABLE = lambda load_type: {Constants.LOAD_TYPE_ASSESSMENT:
                                            Constants.STG_ASMT_OUT_TABLE,
                                            Constants.LOAD_TYPE_STUDENT_REGISTRATION:
                                            Constants.STG_SR_TABLE}.get(load_type, None)
    UDL2_INTEGRATION_TABLE = lambda load_type: {Constants.LOAD_TYPE_ASSESSMENT:
                                                Constants.INT_ASMT_OUT_TABLE,
                                                Constants.LOAD_TYPE_STUDENT_REGISTRATION:
                                                Constants.INT_SR_TABLE}.get(load_type, None)
    UDL2_JSON_INTEGRATION_TABLE = lambda load_type: {Constants.LOAD_TYPE_ASSESSMENT:
                                                     Constants.INT_ASMT_TABLE,
                                                     Constants.LOAD_TYPE_STUDENT_REGISTRATION:
                                                     Constants.INT_SR_META_TABLE}.get(load_type, None)
    UDL2_REF_MAPPING_TABLE = lambda load_type: {Constants.LOAD_TYPE_ASSESSMENT:
                                                Constants.ASMT_REF_TABLE,
                                                Constants.LOAD_TYPE_STUDENT_REGISTRATION:
                                                Constants.SR_REF_TABLE}.get(load_type, None)

    TENANT_SEQUENCE_NAME = lambda tenant: Constants.SEQUENCE_NAME + '_' + tenant if tenant is not None and len(tenant) > 0 else None

    IDENTIFICATION_GUID = 'identification.guid'
    SOURCE_TESTREGSYSID = 'source.testregsysid'
    SOURCE_TESTREGCALLBACKURL = 'source.testregcallbackurl'
    IDENTIFICATION_ACADEMICYEAR = 'identification.academicyear'
    EMAIL_NOTIFICATION = 'source.emailnotification'
    SOURCE_CALLBACKURL = 'source.callbackurl'
