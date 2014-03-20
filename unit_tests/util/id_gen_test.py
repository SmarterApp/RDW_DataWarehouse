"""
Unit tests for the project.sbac.util.id_gen module.

@author: nestep
@date: March 20, 2014
"""

import re

import sbac_data_generation.util.id_gen as sbac_id_gen


def test_sr_uuid():
    assert re.match('[a-f0-9]{30}', sbac_id_gen.get_sr_uuid())