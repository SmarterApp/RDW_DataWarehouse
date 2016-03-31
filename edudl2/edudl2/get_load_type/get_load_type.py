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

import logging
from edudl2.json_util.json_util import get_value_from_json
from edudl2.udl2.constants import Constants

__author__ = 'tshewchuk'

logger = logging.getLogger(__name__)
load_types = Constants.LOAD_TYPES()


def get_load_type(json_file_dir):
    """
    Get the load type for this UDL job from the json file
    @param json_file_dir: A directory that houses the json file
    @return: UDL job load type
    @rtype: string
    """

    load_type = get_value_from_json(json_file_dir, Constants.LOAD_TYPE_KEY).lower()

    if load_type not in load_types:
        raise ValueError('No valid load type specified in json file --')

    return load_type
