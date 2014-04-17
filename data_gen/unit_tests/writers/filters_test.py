"""
Unit tests for the project.sbac.writers.filters module.

@author: nestep
@date: March 20, 2014
"""

import sbac_data_generation.writers.filters as sbac_filters


def test_filter_yesno_true():
    assert sbac_filters.filter_yesno(True) == 'Yes'


def test_filter_yesno_false():
    assert sbac_filters.filter_yesno(False) == 'No'


def test_filter_yesno_none():
    assert sbac_filters.filter_yesno(None) == 'No'


def test_filter_yesnoblank_true():
    assert sbac_filters.filter_yesnoblank(True) == 'Yes'


def test_filter_yesnoblank_false_hundred_thousand():
    count_blank = 0
    for _ in range(100000):
        if sbac_filters.filter_yesnoblank(False) == '':
            count_blank += 1

    assert .07 < (count_blank / 100000) < .09


def test_filter_always_true_true():
    assert sbac_filters.filter_always_true(True)


def test_filter_always_true_false():
    assert sbac_filters.filter_always_true(False)


def test_filter_always_true_none():
    assert sbac_filters.filter_always_true(None)


def test_filter_only_delete_create():
    assert sbac_filters.filter_only_delete('C') is None


def test_filter_only_delete_inactive():
    assert sbac_filters.filter_only_delete('I') is None


def test_filter_only_delete_delete():
    assert sbac_filters.filter_only_delete('D') == 'D'


def test_filter_only_delete_none():
    assert sbac_filters.filter_only_delete(None) is None


def test_filter_twenty_characters_none():
    assert sbac_filters.filter_twenty_characters(None) is None


def test_filter_twenty_characters_short():
    val = 'abc'
    filtered = sbac_filters.filter_twenty_characters(val)
    assert len(filtered) == 3
    assert val == filtered


def test_filter_twenty_characters_twenty():
    val = 'abcdefjdiadndifiejad'
    filtered = sbac_filters.filter_twenty_characters(val)
    assert len(filtered) == 20
    assert val == filtered


def test_filter_twenty_characters_long():
    val = 'abcdefjdiadndifiejaddfed'
    expect_filtered = 'abcdefjdiadndifiejad'
    filtered = sbac_filters.filter_twenty_characters(val)
    assert len(filtered) == 20
    assert filtered == expect_filtered


def test_filter_zero_pad_grade_none():
    assert sbac_filters.filter_zero_padded_grade(None) == '00'


def test_filter_zero_pad_grade_single_digit():
    assert sbac_filters.filter_zero_padded_grade(1) == '01'


def test_filter_zero_pad_grade_double_digit():
    assert sbac_filters.filter_zero_padded_grade(11) == '11'