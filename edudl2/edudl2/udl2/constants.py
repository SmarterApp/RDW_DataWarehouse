__author__ = 'sravi'


class Constants():
    """
    constants related to udl db schema
    """
    # schema names

    # table names
    SR_TARGET_TABLE = 'student_reg'
    UDL2_STAGING_ASSESSMENT_TABLE = 'stg_sbac_asmt_outcome'
    UDL2_STAGING_STUDENT_REGISTRATION_TABLE = 'stg_sbac_stu_reg'

    # column names

    # column values
    OP_COLUMN_NAME = 'op'

    LOAD_TYPE_KEY = 'content'
    LOAD_TYPE_ASSESSMENT = 'assessment'
    LOAD_TYPE_STUDENT_REGISTRATION = 'studentregistration'

    # lambdas for returning list of constants or constants based on some condition
    # TODO: in future this will be replaced with dynamic udl schema based on load being processed
    LOAD_TYPES = lambda: [Constants.LOAD_TYPE_ASSESSMENT, Constants.LOAD_TYPE_STUDENT_REGISTRATION]
    UDL2_STAGING_TABLE = lambda load_type: {Constants.LOAD_TYPE_ASSESSMENT:
                                            Constants.UDL2_STAGING_ASSESSMENT_TABLE,
                                            Constants.LOAD_TYPE_STUDENT_REGISTRATION:
                                            Constants.UDL2_STAGING_STUDENT_REGISTRATION_TABLE}.get(load_type, None)
