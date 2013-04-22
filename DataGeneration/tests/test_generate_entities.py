import unittest
import constants_2 as constants
from datetime import date
from uuid import UUID
from generate_entities import generate_institution_hierarchy, generate_student, generate_section, generate_staff, \
    generate_assessment

class TestGenerateEntities(unittest.TestCase):

    def test_generate_institution_hierarchy(self):
        params = {
            'state_name': 'New York',
            'state_code': 'NY',
            'district_guid': 1,
            'district_name': 'district_1',
            'school_guid': 2,
            'school_name': 'school_2',
            'school_category': 'High School',
            'from_date':  date(2013, 4, 15),
            'most_recent':  True
        }
        institution_hierarchy = generate_institution_hierarchy(**params)
        self.assertEquals(institution_hierarchy.state_name, params['state_name'])
        self.assertEquals(institution_hierarchy.state_code, params['state_code'])
        self.assertEquals(institution_hierarchy.district_guid, params['district_guid'])
        self.assertEquals(institution_hierarchy.district_name, params['district_name'])
        self.assertEquals(institution_hierarchy.school_guid, params['school_guid'])
        self.assertEquals(institution_hierarchy.school_name, params['school_name'])
        self.assertEquals(institution_hierarchy.school_category, params['school_category'])
        self.assertEquals(institution_hierarchy.from_date, params['from_date'])
        self.assertEquals(institution_hierarchy.most_recent, params['most_recent'])
        self.assertIsInstance(institution_hierarchy.inst_hier_rec_id, int)

    def test_generate_student(self):
        params = {
            'section_guid': 1,
            'grade': 9,
            'state_code': 'NY',
            'district_guid': 2,
            'school_guid': 3,
            'school_name': 'school_2',
            'street_names': ['Suffolk', 'President', 'Allen'],
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        student = generate_student(**params)
        self.assertIsInstance(student.student_rec_id, int)
        self.assertIsInstance(student.student_guid, UUID)
        self.assertIsInstance(student.first_name, str)
        self.assertIsInstance(student.last_name, str)
        address_component_words = student.address_1.split()
        address= int(address_component_words[0])
        street_name = address_component_words[1]
        suffix = address_component_words[2].upper()
        self.assertIsInstance(address, int)
        self.assertIn(street_name, params['street_names'])
        self.assertIn(suffix, constants.ADD_SUFFIX)
        city_component_words = student.city.split()
        city_name_1 = city_component_words[0]
        city_name_2 = city_component_words[1]
        self.assertIn(city_name_1, params['street_names'])
        self.assertIn(city_name_2, params['street_names'])
        self.assertIsInstance(student.zip_code, int)
        self.assertIn(student.gender, constants.GENDERS)
        self.assertIsInstance(student.email, str)
        self.assertIsInstance(student.dob, str)
        self.assertEquals(student.section_guid, params['section_guid'])
        self.assertEquals(student.grade, params['grade'])
        self.assertEquals(student.state_code, params['state_code'])
        self.assertEquals(student.district_guid, params['district_guid'])
        self.assertEquals(student.school_guid, params['school_guid'])
        self.assertIsInstance(student.from_date, date)
        self.assertIsInstance(student.most_recent, bool)


    def test_generate_section(self):
        params = {
            'subject_name': 'ELA',
            'grade': 9,
            'state_code': 'NY',
            'district_guid': 1,
            'school_guid': 2,
            'section_number': 1,
            'class_number': 2,
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        section = generate_section(**params)
        self.assertIsInstance(section.section_rec_id, int)
        self.assertIsInstance(section.section_guid, UUID)
        section_component_words = section.section_name.split()
        section_name = section_component_words[0]
        section_number = section_component_words[1]
        self.assertEquals(section_name, 'Section')
        self.assertEquals(int(section_number), params['section_number'])
        self.assertEquals(section.grade, params['grade'])
        class_component_words = section.class_name.split('_')
        class_name = class_component_words[0]
        class_number = int(class_component_words[1])
        self.assertEquals(class_name, params['subject_name'])
        self.assertEquals(class_number, params['class_number'])

        '''
        self.class_name, self.subject_name, self.state_code, self.district_guid, self.school_guid, self.from_date, self.to_date, self.most_recent
        '''

    def test_generate_assessment(self):
        params = {
            'asmt_type': 'Summative',
            'asmt_period': 'Spring',
            'asmt_period_year': 2012,
            'asmt_subject': 'Math',
            'asmt_grade': 9,
            'asmt_cut_point_1': 1400,
            'asmt_cut_point_2': 1800,
            'asmt_cut_point_3': 2100,
            'asmt_cut_point_4': 2200,
            'from_date': date(2013, 4, 15),
            'most_recent': True,
        }

        a = generate_assessment(**params)
        self.assertIsInstance(a.asmt_rec_id, int)
        self.assertIsInstance(a.asmt_guid, UUID)
        self.assertEquals(a.asmt_type, params['asmt_type'])


    def test_generate_staff(self):
        params = {
            'hier_user_type': 'Staff',
            'state_code': 'NY',
            'district_guid': 1,
            'school_guid': 2,
            'section_guid': 3,
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }

        staff = generate_staff(**params)
        self.assertIsInstance(staff.staff_rec_id, int)
        self.assertIsInstance(staff.staff_guid, UUID)
        self.assertIsInstance(staff.first_name, str)
        self.assertIsInstance(staff.last_name, str)
        self.assertEquals(staff.section_guid, params['section_guid'])
        self.assertEquals(staff.hier_user_type, params['hier_user_type'])
        self.assertEquals(staff.state_code, params['state_code'])
        self.assertEquals(staff.district_guid, params['district_guid'])
        self.assertEquals(staff.school_guid, params['school_guid'])
        self.assertIsInstance(staff.from_date, date)
        self.assertIsInstance(staff.most_recent, bool)



