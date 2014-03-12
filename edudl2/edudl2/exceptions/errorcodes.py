"""
This module contains UDL2 error code. that will be returned to the caller when
an error has been encountered. Error codes can be used by the caller to display
specific error messages depending on the UDL failure reason.
"""


class ErrorCode(object):
    # system code
    NOT_IMPLEMENTED = '-1'
    STATUS_OK = '0'
    STATUS_FAIL = '-2'
    STATUS_UNKNOWN_ERROR = '-3'

    # Error Codes related to csv_validator.py and json_validator.py
    SRC_FOLDER_NOT_ACCESSIBLE_SFV = '3001'
    SRC_FILE_NOT_ACCESSIBLE_SFV = '3002'
    SRC_FILE_HAS_NO_DATA = '3003'

    # This code has changed
    SRC_CSV_OR_JSON_DOESNT_EXIST = '3004'

    SRC_FILE_WRONG_DELIMITER = '3005'
    SRC_FILE_HAS_HEADERS_MISMATCH_EXPECTED_FORMAT = '3006'
    SRC_FILE_HEADERS_MISMATCH_DATA = '3008'
    SRC_FILE_HAS_NO_HEADERS = '3009'
    SRC_FILE_TYPE_NOT_SUPPORTED = '3010'
    SRC_FILE_HAS_DUPLICATE_HEADERS = '3011'

    # Newly added codes
    SRC_JSON_INVALID_STRUCTURE = '3012'
    SRC_JSON_INVALID_FORMAT = '3013'
    # For UDL insert and delete

    DELETE_RECORD_NOT_FOUND = '1000'
    BATCH_REC_FAILED = '2005'
    DATA_INTEGRITY_ERROR = '1001'


class ErrorCodeMessage(object):
    messages = {
        # system code
        '-1': 'NOT_IMPLEMENTED',
        '0': 'STATUS_OK',
        '-2': 'STATUS_FAIL',
        '-3': 'STATUS_UNKNOWN_ERROR',

        # Error Codes related to csv_validator.py and json_validator.py
        '3001': 'SRC_FOLDER_NOT_ACCESSIBLE_SFV',
        '3002': 'SRC_FILE_NOT_ACCESSIBLE_SFV',
        '3003': 'SRC_FILE_HAS_NO_DATA',

        # This code has changed
        '3004': 'SRC_CSV_OR_JSON_DOESNT_EXIST',
        '3005': 'SRC_FILE_WRONG_DELIMITER',
        '3006': 'SRC_FILE_HAS_HEADERS_MISMATCH_EXPECTED_FORMAT',
        '3008': 'SRC_FILE_HEADERS_MISMATCH_DATA',
        '3009': 'SRC_FILE_HAS_NO_HEADERS',
        '3010': 'SRC_FILE_TYPE_NOT_SUPPORTED',
        '3011': 'SRC_FILE_HAS_DUPLICATE_HEADERS',

        # Newly added codes
        '3012': 'SRC_JSON_INVALID_STRUCTURE',
        '3013': 'SRC_JSON_INVALID_FORMAT',
        # For UDL insert and delete

        '1000': 'DELETE_RECORD_NOT_FOUND',
        '2005': 'BATCH_REC_FAILED',
        '1001': 'DATA_INTEGRITY_ERROR',
    }

    @classmethod
    def getText(cls, code):
        try:
            message = cls.messages[code]
        except KeyError:
            message = ''
        return message
