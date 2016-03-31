# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Apr 7, 2014

@author: tosako
'''


class UDL2Exception(Exception):
    '''
    generic UDL2 exception
    '''
    def __init__(self, msg='UDL2 Generic Exception'):
        self.__msg = msg

    def __str__(self):
        return repr(self.__msg)


class UDL2SQLFilteredSQLStringException(UDL2Exception):
    '''
    SQL query string contains invalid character.
    '''
    def __init__(self, msg='UDL2 Filtered SQL String Exception'):
        super().__init__(msg)


class UDL2GlobalSequenceMissingException(UDL2Exception):
    """
    Production database is missing Global Sequence
    """
    def __init__(self, msg='UDL2 Prod Global Sequence Missing'):
        super().__init__(msg)


class UDL2DataValidationException(UDL2Exception):
    """
    Production database is missing Global Sequence
    """
    def __init__(self, msg='UDL2 Data Validation Failed'):
        super().__init__(msg)


class UDL2InvalidJSONCSVPairException(UDL2DataValidationException):
    """
    Production database is missing Global Sequence
    """
    def __init__(self, msg='UDL2 JSON and CSV file mismatch for asmt_guid'):
        super().__init__(msg)


class InvalidTenantNameException(UDL2DataValidationException):
    """
    Production database is missing Global Sequence
    """
    def __init__(self, msg='UDL2 tenant name invalid'):
        super().__init__(msg)


class UDL2DataLoadingException(UDL2Exception):
    '''
    Loading data exception
    '''
    def __init__(self, msg='failed to load all data'):
        super().__init__(msg)
