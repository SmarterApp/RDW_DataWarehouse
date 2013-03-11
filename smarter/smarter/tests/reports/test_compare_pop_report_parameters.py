'''
Created on Mar 8, 2013

@author: tosako
'''
import unittest
from smarter.reports.compare_pop_report import Constants, Parameters,\
    ParameterManager


class Test(unittest.TestCase):

    def test_Parameter_school(self):
        parameters = Parameters(get_param_school_view())
        self.assertEqual('AB', parameters.state_id)
        self.assertEqual('CD', parameters.district_id)
        self.assertEqual('EF', parameters.school_id)

    def test_Parameter_district(self):
        parameters = Parameters(get_param_district_view())
        self.assertEqual('AB', parameters.state_id)
        self.assertEqual('CD', parameters.district_id)
        self.assertIsNone(parameters.school_id)

    def test_Parameter_state(self):
        parameters = Parameters(get_param_state_view())
        self.assertEqual('AB', parameters.state_id)
        self.assertIsNone(parameters.district_id)
        self.assertIsNone(parameters.school_id)

    def test_ParameterManager_school_view(self):
        manager = ParameterManager(Parameters(get_param_school_view()))
        self.assertTrue(manager.is_school_view())
        self.assertFalse(manager.is_district_view())
        self.assertFalse(manager.is_state_view())

    def test_ParameterManager_district_view(self):
        manager = ParameterManager(Parameters(get_param_district_view()))
        self.assertFalse(manager.is_school_view())
        self.assertTrue(manager.is_district_view())
        self.assertFalse(manager.is_state_view())

    def test_ParameterManager_state_view(self):
        manager = ParameterManager(Parameters(get_param_state_view()))
        self.assertFalse(manager.is_school_view())
        self.assertFalse(manager.is_district_view())
        self.assertTrue(manager.is_state_view())

    def test_ParameterManager_school_field_name(self):
        manager = ParameterManager(Parameters(get_param_school_view()))
        self.assertEqual(Constants.ASMT_GRADE, manager.get_name_of_field())

    def test_ParameterManager_district_field_name(self):
        manager = ParameterManager(Parameters(get_param_district_view()))
        self.assertEqual(Constants.SCHOOL_NAME, manager.get_name_of_field())

    def test_ParameterManager_state_field_name(self):
        manager = ParameterManager(Parameters(get_param_state_view()))
        self.assertEqual(Constants.DISTRICT_NAME, manager.get_name_of_field())

    def test_ParameterManager_school_id_name(self):
        manager = ParameterManager(Parameters(get_param_school_view()))
        self.assertEqual(Constants.ASMT_GRADE, manager.get_id_of_field())

    def test_ParameterManager_district_id_name(self):
        manager = ParameterManager(Parameters(get_param_district_view()))
        self.assertEqual(Constants.SCHOOL_ID, manager.get_id_of_field())

    def test_ParameterManager_state_id_name(self):
        manager = ParameterManager(Parameters(get_param_state_view()))
        self.assertEqual(Constants.DISTRICT_ID, manager.get_id_of_field())

    def test_ParameterManager_property(self):
        params1 = get_param_school_view()
        params2 = get_param_district_view()
        manager1 = ParameterManager(params1)
        manager1_1 = ParameterManager(params1)
        manager2 = ParameterManager(params2)
        self.assertEqual(manager1.p, manager1_1.p)
        self.assertEqual(manager2.p, manager2.p)
        self.assertNotEqual(manager1.p, manager2.p)


def get_param_school_view():
    return {Constants.STATEID: 'AB', Constants.DISTRICTID: 'CD', Constants.SCHOOLID: 'EF'}


def get_param_district_view():
    return {Constants.STATEID: 'AB', Constants.DISTRICTID: 'CD'}


def get_param_state_view():
    return {Constants.STATEID: 'AB'}


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
