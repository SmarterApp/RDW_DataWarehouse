import unittest
import constants_2 as constants
from datetime import date
from generate_entities import generate_institution_hierarchy, generate_student, generate_section

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
        self.assertIsInstance(institution_hierarchy.inst_hier_rec_id, str)

    def test_generate_student(self):
        params = {
            'section_guid': 1,
            'grade': 9,
            'state_code': 'NY',
            'district_guid': 2,
            'school_guid': 3,
            'school_name': 'school_2',
            'street_names': ['Suffolk', 'President', 'Allen']
        }
        student = generate_student(**params)
        self.assertIsInstance(student.student_rec_id, str)
        self.assertIsInstance(student.student_guid, int)
        self.assertIsInstance(student.first_name, str)
        self.assertIsInstance(student.last_name, str)
        component_words = student.address_1.split()
        address= component_words[0]
        street_name = component_words[1]
        suffix = component_words[2]
        self.assertIsInstance(address, int)
        self.assertIn(street_name, params['street_names'])
        self.assertIn(suffix, constants.ADD_SUFFIX)
        self.assertIn(student.city, params['street_names'])
        self.assertIsInstance(student.zip_code, int)
        self.assertIn(student.gender, constants.GENDERS)
        self.assertIsInstance(student.email, str)
        self.assertIsInstance(student.dob, date)
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
            'class_number': 2
        }
        section = generate_section(**params)
        self.assertIsInstance(section.section_rec_id, str)
        self.assertIsInstance(section.section_guid, int)
        section_component_words = section.section_name.split()
        section_name = section_component_words[0]
        section_number = section_component_words[1]
        self.assertEquals(section_name, 'Section')
        self.assertEquals(section_number, params['section_number'])
        self.assertEquals(section.grade, params['grade'])
        class_component_words = section.class_name.split()
        class_name = class_component_words[0]
        class_number = class_component_words[1]
        self.assertEquals(class_name, 'Class')
        self.assertEquals(class_number, params['class_numbfer'])

        '''
        self.class_name, self.subject_name, self.state_code, self.district_guid, self.school_guid, self.from_date, self.to_date, self.most_recent
        '''

