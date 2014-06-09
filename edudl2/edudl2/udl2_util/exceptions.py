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
