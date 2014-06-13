"""
Unit tests for the project.sbac.util.id_gen module.

@author: nestep
@date: March 20, 2014
"""

import re

from nose.tools import assert_is_instance, assert_regexp_matches

from sbac_data_generation.util.id_gen import IDGen

GUID_REGEX = '[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}'
SR_GUID_REGEX = '[a-f0-9]{30}'


def test_rec_id():
    idg = IDGen()
    id = idg.get_rec_id('some_object_type')
    assert_is_instance(id, int)
    assert id == 100000000000


def test_rec_id_from_two_types():
    idg = IDGen()
    assert idg.get_rec_id('some_object_type_1') == 100000000000
    assert idg.get_rec_id('some_object_type_2') == 100000000000


def test_guid():
    idg = IDGen()
    assert re.match(GUID_REGEX, idg.get_uuid())


def test_sr_uuid():
    idg = IDGen()
    assert_regexp_matches(idg.get_sr_uuid(), SR_GUID_REGEX)
