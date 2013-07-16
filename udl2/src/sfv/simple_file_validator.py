from __future__ import absolute_import

"""
Simple File Validator job performs the basic validations on the incoming
Assessment file.

Some of the basic validations include (but not limited to)
a) Checking the file is valid
b) Checking the file has data and the application has permissions to access it
"""

import os

from sfv import error_codes
from sfv import csv_validator
from sfv import json_validator
from udl2_util.measurement import measure_cpu_plus_elasped_time


class SimpleFileValidator():
    """Determines the file extension and invokes a suite of validations"""

    @measure_cpu_plus_elasped_time
    def __init__(self):
        """Constructor"""
        self.validators = {'.csv': csv_validator.CsvValidator(),
                           '.json': json_validator.JsonValidator(),
                           }

    @measure_cpu_plus_elasped_time
    def execute(self, dir_path, file_name, guid_batch):
        """Check the file extension and invokes the appropriate Validator
        :param dir_path: path of the file
        :type dir_path: string
        :param file_name: name of the file
        :type file_name: string
        :param guid_batch: batch id of the file
        :type guid_batch: integer
        :return: tuple of the form: (status_code, dir_path, file_name, guid_batch)
        """
        # Get the file extension
        extension = os.path.splitext(file_name)[1]

        # Get the corresponding validator and check
        validator = self.validators.get(extension, None)

        if validator:
            result = validator.execute(dir_path, file_name, guid_batch)
            return result
        else:
            return [(error_codes.SRC_FILE_TYPE_NOT_SUPPORTED,
                    dir_path,
                    file_name,
                    guid_batch)]
