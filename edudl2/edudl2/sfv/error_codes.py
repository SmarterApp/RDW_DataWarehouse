from __future__ import absolute_import

"""
This module contains error code constants that will be returned to the caller when
an error has been encountered. Error codes can be used by the caller to display
specific error messages depending on the UDL failure reason.
"""

# Global
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
