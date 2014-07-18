import unittest
import DataGeneration.src.constants.constants as constants
from datetime import date
from uuid import UUID, uuid4
from DataGeneration.src.generators.generate_entities import (generate_institution_hierarchy, generate_student, generate_section, generate_staff,
                                                             generate_assessment, generate_students, generate_sections, generate_assessments,
                                                             generate_multiple_staff, generate_students_from_student_info,
                                                             generate_assessment_outcomes_from_student_info)
from DataGeneration.src.models.entities import Student, Section, Assessment, Staff


class TestGenerateEntities(unittest.TestCase):

    def test_generate_students_from_student_info(self):
        student_info1 = DummyClass(student_rec_ids=[1, 2], student_id='g123', section_guids={'Math': 'm123', 'ELA': 'e123'},
                                   first_name='Bob', last_name='Smith', address_1='add1', city='city1', zip_code=12345, gender='male',
                                   email='bob.smith@email.com', dob=date(2005, 12, 5), grade=2, state_code='GA', district_id='d123',
                                   school_id='s123', from_date=date.today(), most_recent=True, middle_name='James', to_date=None,
                                   asmt_scores={'Math': None, 'ELA': None})
        student_info2 = DummyClass(student_rec_ids=[3, 4], student_id='g456', section_guids={'Math': 'm123', 'ELA': 'e568'},
                                   first_name='Lili', last_name='Chen', address_1='add89', city='Seattle', zip_code=12345, gender='female',
                                   email='lili.chen@email.com', dob=date(2005, 12, 5), grade=2, state_code='WA', district_id='d568',
                                   school_id='s5872', from_date=date.today(), most_recent=True, middle_name=None, to_date=None,
                                   asmt_scores={'Math': None, 'ELA': None})
        students = generate_students_from_student_info([student_info1, student_info2])
        self.assertEqual(len(students), 4)

    def test_generate_students_from_student_info_2(self):
        student_info1 = DummyClass(student_rec_ids=[1, 2], student_id='g123', section_guids={'Math': 'm123', 'ELA': 'e123'},
                                   first_name='Bob', last_name='Smith', address_1='add1', city='city1', zip_code=12345, gender='male',
                                   email='bob.smith@email.com', dob=date(2005, 12, 5), grade=2, state_code='GA', district_id='d123',
                                   school_id='s123', from_date=date.today(), most_recent=True, middle_name='James', to_date=None,
                                   asmt_scores={'Math': None, 'ELA': None})
        student_info2 = DummyClass(student_rec_ids=[3], student_id='g456', section_guids={'ELA': 'e568'},
                                   first_name='Bobbi', last_name='Brown', address_1='add89', city='Seattle', zip_code=12345, gender='female',
                                   email='bobbi.brown@email.com', dob=date(2005, 12, 5), grade=2, state_code='WA', district_id='d568',
                                   school_id='s5872', from_date=date.today(), most_recent=True, middle_name=None, to_date=None,
                                   asmt_scores={'ELA': None})

        students = generate_students_from_student_info([student_info1, student_info2])
        self.assertEqual(len(students), 3)

    def test_generate_students_from_student_info_check_values(self):
        student_info1 = DummyClass(student_rec_ids=[1, 2], student_id='g123', section_guids={'Math': 'm123', 'ELA': 'e123'},
                                   first_name='Bob', last_name='Smith', address_1='add1', city='city1', zip_code=12345, gender='male',
                                   email='bob.smith@email.com', dob=date(2005, 12, 5), grade=2, state_code='GA', district_id='d123',
                                   school_id='s123', from_date=date.today(), most_recent=True, middle_name='James', to_date=None,
                                   asmt_scores={'Math': None, 'ELA': None})

        students = generate_students_from_student_info([student_info1])

        for student in students:
            self.assertIn(student.student_rec_id, [1, 2])
            self.assertEqual(student.student_id, 'g123')
            self.assertEqual(student.first_name, 'Bob')
            self.assertEqual(student.address_1, 'add1')
            self.assertEqual(student.city, 'city1')
            self.assertEqual(student.zip_code, 12345)
            self.assertEqual(student.gender, 'male')
            self.assertEqual(student.email, 'bob.smith@email.com')
            self.assertEqual(student.dob, date(2005, 12, 5))
            self.assertIn(student.section_guid, ['m123', 'e123'])
            self.assertEqual(student.grade, 2)
            self.assertEqual(student.state_code, 'GA')
            self.assertEqual(student.district_id, 'd123')
            self.assertEqual(student.school_id, 's123')
            self.assertEqual(student.from_date, date.today())
            self.assertIsNone(student.to_date)
            self.assertTrue(student.most_recent)
            self.assertIsNone(student.to_date)

    def test_generate_assessment_outcomes_from_student_info(self):
        claim_scores1 = [DummyClass(claim_score=1300 + i, claim_score_interval_minimum=1200, claim_score_interval_maximum=1400, perf_lvl=1) for i in range(3)]
        claim_scores2 = [DummyClass(claim_score=1500 + i, claim_score_interval_minimum=1200, claim_score_interval_maximum=1800, perf_lvl=1) for i in range(4)]
        asmt_scores1 = {'Math': DummyClass(overall_score=2300, interval_min=2200, interval_max=2400, perf_lvl=4, claim_scores=claim_scores1),
                        'ELA': DummyClass(overall_score=1500, interval_min=1400, interval_max=1600, perf_lvl=2, claim_scores=claim_scores2)}
        student_info1 = DummyClass(student_rec_ids=[1, 2], student_id='g123', section_guids={'Math': 'm123', 'ELA': 'e123'},
                                   first_name='Bob', last_name='Smith', address_1='add1', city='city1', zip_code=12345, gender='male',
                                   email='bob.smith@email.com', dob=date(2005, 12, 5), grade=2, state_code='GA', district_id='d123',
                                   school_id='s123', from_date=date.today(), most_recent=True, middle_name='James', to_date=None,
                                   #other
                                   asmt_rec_ids={'Math': 'Masmt1', 'ELA': 'Easmt1'}, teacher_guids={'Math': 'Mteach1', 'ELA': 'Eteach1'},
                                   section_rec_ids={'Math': 'MRsec1', 'ELA': 'ERsec1'}, asmt_scores=asmt_scores1,
                                   asmt_dates_taken={'Math': date(2099, 12, 12), 'ELA': date(2099, 11, 11)},
                                   asmt_types={'Math': "SUMMATIVE", 'ELA': "SUMMATIVE"}, asmt_years={'ELA': '2099', 'Math': "2099"},
                                   asmt_subjects={'ELA': 'ELA', 'Math': "Math"}, dmg_eth_hsp=True, dmg_eth_ami=False, dmg_eth_asn=False, dmg_eth_blk=False,
                                   dmg_eth_pcf=True, dmg_eth_wht=False, dmg_prg_iep=True, dmg_prg_lep=True, dmg_prg_504=True, dmg_prg_tt1=True)
        student_info1.get_stu_demo_list = lambda: [False, False, True, False, False, True, False]
        batch_guid = '00000000-0000-0000-0000-000000000000'
        inst_hier = DummyClass(school_name='School1', inst_hier_rec_id='i5678')
        asmt_outcomes = generate_assessment_outcomes_from_student_info([student_info1], batch_guid, inst_hier)

        self.assertEqual(len(asmt_outcomes), 2)

    def test_generate_assessment_outcomes_from_student_info_2(self):
        claim_scores1 = [DummyClass(claim_score=1300 + i, claim_score_interval_minimum=1200, claim_score_interval_maximum=1400, perf_lvl=1) for i in range(3)]
        claim_scores2 = [DummyClass(claim_score=1500 + i, claim_score_interval_minimum=1200, claim_score_interval_maximum=1800, perf_lvl=1) for i in range(4)]
        asmt_scores1 = {'Math': DummyClass(overall_score=2300, interval_min=2200, interval_max=2400, perf_lvl=4, claim_scores=claim_scores1),
                        'ELA': DummyClass(overall_score=1500, interval_min=1400, interval_max=1600, perf_lvl=2, claim_scores=claim_scores2)}
        student_info1 = DummyClass(student_rec_ids=[1, 2], student_id='g123', section_guids={'Math': 'm123', 'ELA': 'e123'},
                                   first_name='Bob', last_name='Smith', address_1='add1', city='city1', zip_code=12345, gender='male',
                                   email='bob.smith@email.com', dob=date(2005, 12, 5), grade=2, state_code='GA', district_id='d123',
                                   school_id='s123', from_date=date.today(), most_recent=True, middle_name='James', to_date=None,
                                   #other
                                   asmt_rec_ids={'Math': 'Masmt1', 'ELA': 'Easmt1'}, teacher_guids={'Math': 'Mteach1', 'ELA': 'Eteach1'},
                                   section_rec_ids={'Math': 'MRsec1', 'ELA': 'ERsec1'}, asmt_scores=asmt_scores1,
                                   asmt_dates_taken={'Math': date(2099, 12, 12), 'ELA': date(2099, 11, 11)},
                                   asmt_types={'Math': "SUMMATIVE", 'ELA': "SUMMATIVE"}, asmt_years={'ELA': '2099', 'Math': "2099"},
                                   asmt_subjects={'ELA': 'ELA', 'Math': "Math"}, dmg_eth_hsp=True, dmg_eth_ami=False, dmg_eth_asn=False, dmg_eth_blk=False,
                                   dmg_eth_pcf=True, dmg_eth_wht=False, dmg_prg_iep=True, dmg_prg_lep=True, dmg_prg_504=True, dmg_prg_tt1=True)
        student_info2 = DummyClass(student_rec_ids=[1, 2], student_id='g123', section_guids={'Math': 'm123', 'ELA': 'e123'},
                                   first_name='Bob', last_name='Smith', address_1='add1', city='city1', zip_code=12345, gender='male',
                                   email='bob.smith@email.com', dob=date(2005, 12, 5), grade=2, state_code='GA', district_id='d123',
                                   school_id='s123', from_date=date.today(), most_recent=True, middle_name='James', to_date=None,
                                   #other
                                   asmt_rec_ids={'Math': 'Masmt1', 'ELA': 'Easmt1'}, teacher_guids={'Math': 'Mteach1', 'ELA': 'Eteach1'},
                                   section_rec_ids={'Math': 'MRsec1', 'ELA': 'ERsec1'}, asmt_scores=asmt_scores1,
                                   asmt_dates_taken={'Math': date(2099, 12, 12), 'ELA': date(2099, 11, 11)},
                                   asmt_types={'Math': "SUMMATIVE", 'ELA': "SUMMATIVE"}, asmt_years={'ELA': '2099', 'Math': "2099"},
                                   asmt_subjects={'ELA': 'ELA', 'Math': "Math"}, dmg_eth_hsp=True, dmg_eth_ami=False, dmg_eth_asn=False, dmg_eth_blk=False,
                                   dmg_eth_pcf=True, dmg_eth_wht=False, dmg_prg_iep=True, dmg_prg_lep=True, dmg_prg_504=True, dmg_prg_tt1=True)
        student_info1.get_stu_demo_list = lambda: [False, False, True, False, False, True, False]
        student_info2.get_stu_demo_list = lambda: [False, False, True, False, False, True, False]
        batch_guid = '00000000-0000-0000-0000-000000000000'
        inst_hier = DummyClass(school_name='School1', inst_hier_rec_id='i5678')
        asmt_outcomes = generate_assessment_outcomes_from_student_info([student_info1, student_info2], batch_guid, inst_hier)

        self.assertEqual(len(asmt_outcomes), 4)

    def test_generate_assessment_outcomes_from_student_info_3(self):
        claim_scores1 = [DummyClass(claim_score=1300 + i, claim_score_interval_minimum=1200, claim_score_interval_maximum=1400, perf_lvl=1) for i in range(3)]
        asmt_scores1 = {'Math': DummyClass(overall_score=2300, interval_min=2200, interval_max=2400, perf_lvl=4, claim_scores=claim_scores1)}

        student_info1 = DummyClass(student_rec_ids=[1, 2], student_id='g123', section_guids={'Math': 'm123', 'ELA': 'e123'},
                                   first_name='Bob', last_name='Smith', address_1='add1', city='city1', zip_code=12345, gender='male',
                                   email='bob.smith@email.com', dob=date(2005, 12, 5), grade=2, state_code='GA', district_id='d123',
                                   school_id='s123', from_date=date.today(), most_recent=True, middle_name='James', to_date=None,
                                   #other
                                   asmt_rec_ids={'Math': 'Masmt1', 'ELA': 'Easmt1'}, teacher_guids={'Math': 'Mteach1', 'ELA': 'Eteach1'},
                                   section_rec_ids={'Math': 'MRsec1', 'ELA': 'ERsec1'}, asmt_scores=asmt_scores1,
                                   asmt_dates_taken={'Math': date(2099, 12, 12), 'ELA': date(2099, 11, 11)},
                                   asmt_types={'Math': "SUMMATIVE", 'ELA': "SUMMATIVE"}, asmt_years={'ELA': 2199, 'Math': 2099},
                                   asmt_subjects={'ELA': 'ELA', 'Math': "Math"}, dmg_eth_hsp=True, dmg_eth_ami=False, dmg_eth_asn=False, dmg_eth_blk=False,
                                   dmg_eth_pcf=True, dmg_eth_wht=False, dmg_prg_iep=True, dmg_prg_lep=True, dmg_prg_504=True, dmg_prg_tt1=True)
        student_info1.get_stu_demo_list = lambda: [False, False, True, False, False, True, False]
        batch_guid = '00000000-0000-0000-0000-000000000000'
        inst_hier = DummyClass(school_name='School1', inst_hier_rec_id='i5678')
        asmt_outcomes = generate_assessment_outcomes_from_student_info([student_info1], batch_guid, inst_hier)

        self.assertEqual(len(asmt_outcomes), 1)

        asmt_outcome = asmt_outcomes[0]
        self.assertIsNotNone(asmt_outcome.asmt_rec_id)
        self.assertEqual(asmt_outcome.student_id, 'g123')
        self.assertEqual(asmt_outcome.teacher_guid, 'Mteach1')
        self.assertEqual(asmt_outcome.state_code, 'GA')
        self.assertEqual(asmt_outcome.district_id, 'd123')
        self.assertEqual(asmt_outcome.school_id, 's123')
        self.assertEqual(asmt_outcome.section_guid, 'm123')
        self.assertEqual(asmt_outcome.inst_hier_rec_id, 'i5678')
        self.assertEqual(asmt_outcome.section_rec_id, 'MRsec1')
        self.assertEqual(asmt_outcome.where_taken_id, 's123')
        self.assertEqual(asmt_outcome.where_taken_name, 'School1')
        self.assertEqual(asmt_outcome.asmt_grade, 2)
        self.assertEqual(asmt_outcome.enrl_grade, 2)
        self.assertEqual(asmt_outcome.date_taken, date(2099, 12, 12).strftime('%Y%m%d'))
        self.assertEqual(asmt_outcome.date_taken_day, date(2099, 12, 12).day)
        self.assertEqual(asmt_outcome.date_taken_month, date(2099, 12, 12).month)
        self.assertEqual(asmt_outcome.date_taken_year, date(2099, 12, 12).year)
        self.assertEqual(asmt_outcome.asmt_score, 2300)
        self.assertEqual(asmt_outcome.asmt_score_range_min, 2200)
        self.assertEqual(asmt_outcome.asmt_score_range_max, 2400)
        self.assertEqual(asmt_outcome.asmt_perf_lvl, 4)
        self.assertEqual(asmt_outcome.asmt_claim_1_score, 1300)
        self.assertEqual(asmt_outcome.asmt_claim_1_score_range_min, 1200)
        self.assertEqual(asmt_outcome.asmt_claim_1_score_range_max, 1400)
        self.assertEqual(asmt_outcome.asmt_claim_2_score, 1301)
        self.assertEqual(asmt_outcome.asmt_claim_2_score_range_min, 1200)
        self.assertEqual(asmt_outcome.asmt_claim_2_score_range_max, 1400)
        self.assertEqual(asmt_outcome.asmt_claim_3_score, 1302)
        self.assertEqual(asmt_outcome.asmt_claim_3_score_range_min, 1200)
        self.assertEqual(asmt_outcome.asmt_claim_3_score_range_max, 1400)
        self.assertIsNone(asmt_outcome.asmt_claim_4_score)
        self.assertIsNone(asmt_outcome.asmt_claim_4_score_range_min)
        self.assertIsNone(asmt_outcome.asmt_claim_4_score_range_max)
        self.assertEqual(asmt_outcome.status, 'C')
        self.assertTrue(asmt_outcome.most_recent)
        self.assertEqual(asmt_outcome.batch_guid, batch_guid)
        self.assertEqual(asmt_outcome.asmt_type, "SUMMATIVE")
        self.assertEqual(asmt_outcome.asmt_year, 2099)
        self.assertEqual(asmt_outcome.asmt_subject, 'Math')
        self.assertEqual(asmt_outcome.gender, 'male')
        self.assertTrue(asmt_outcome.dmg_eth_hsp)
        self.assertFalse(asmt_outcome.dmg_eth_ami)
        self.assertFalse(asmt_outcome.dmg_eth_asn)
        self.assertFalse(asmt_outcome.dmg_eth_blk)
        self.assertTrue(asmt_outcome.dmg_eth_pcf)
        self.assertFalse(asmt_outcome.dmg_eth_wht)
        self.assertTrue(asmt_outcome.dmg_prg_iep)
        self.assertTrue(asmt_outcome.dmg_prg_lep)
        self.assertTrue(asmt_outcome.dmg_prg_504)
        self.assertTrue(asmt_outcome.dmg_prg_tt1)
        self.assertEqual(asmt_outcome.dmg_eth_derived, 3)

    def test_generate_assessment_outcomes_from_student_info_4(self):
        claim_scores1 = [DummyClass(claim_score=1300 + i, claim_score_interval_minimum=1200, claim_score_interval_maximum=1400, perf_lvl=1) for i in range(4)]
        asmt_scores1 = {'Math': DummyClass(overall_score=2300, interval_min=2200, interval_max=2400, perf_lvl=4, claim_scores=claim_scores1)}

        student_info1 = DummyClass(student_rec_ids=[1, 2], student_id='g123', section_guids={'Math': 'm123', 'ELA': 'e123'},
                                   first_name='Bob', last_name='Smith', address_1='add1', city='city1', zip_code=12345, gender='male',
                                   email='bob.smith@email.com', dob=date(2005, 12, 5), grade=2, state_code='GA', district_id='d123',
                                   school_id='s123', from_date=date.today(), most_recent=True, middle_name='James', to_date=None,
                                   #other
                                   asmt_rec_ids={'Math': 'Masmt1', 'ELA': 'Easmt1'}, teacher_guids={'Math': 'Mteach1', 'ELA': 'Eteach1'},
                                   section_rec_ids={'Math': 'MRsec1', 'ELA': 'ERsec1'}, asmt_scores=asmt_scores1,
                                   asmt_dates_taken={'Math': date(2099, 12, 12), 'ELA': date(2099, 11, 11)},
                                   asmt_types={'Math': "SUMMATIVE", 'ELA': "SUMMATIVE"}, asmt_years={'ELA': 2199, 'Math': 2099},
                                   asmt_subjects={'ELA': 'ELA', 'Math': "Math"}, dmg_eth_hsp=True, dmg_eth_ami=False, dmg_eth_asn=False, dmg_eth_blk=False,
                                   dmg_eth_pcf=True, dmg_eth_wht=False, dmg_prg_iep=True, dmg_prg_lep=True, dmg_prg_504=True, dmg_prg_tt1=True)
        student_info1.get_stu_demo_list = lambda: [False, False, True, False, False, True, False]
        batch_guid = '00000000-0000-0000-0000-000000000000'
        inst_hier = DummyClass(school_name='School1', inst_hier_rec_id='i5678')
        asmt_outcomes = generate_assessment_outcomes_from_student_info([student_info1], batch_guid, inst_hier)

        asmt_outcome = asmt_outcomes[0]

        self.assertEqual(asmt_outcome.asmt_claim_1_score, 1300)
        self.assertEqual(asmt_outcome.asmt_claim_1_score_range_min, 1200)
        self.assertEqual(asmt_outcome.asmt_claim_1_score_range_max, 1400)
        self.assertEqual(asmt_outcome.asmt_claim_2_score, 1301)
        self.assertEqual(asmt_outcome.asmt_claim_2_score_range_min, 1200)
        self.assertEqual(asmt_outcome.asmt_claim_2_score_range_max, 1400)
        self.assertEqual(asmt_outcome.asmt_claim_3_score, 1302)
        self.assertEqual(asmt_outcome.asmt_claim_3_score_range_min, 1200)
        self.assertEqual(asmt_outcome.asmt_claim_3_score_range_max, 1400)
        self.assertEqual(asmt_outcome.asmt_claim_4_score, 1303)
        self.assertEqual(asmt_outcome.asmt_claim_4_score_range_min, 1200)
        self.assertEqual(asmt_outcome.asmt_claim_4_score_range_max, 1400)

    def test_generate_institution_hierarchy(self):
        params = {
            'state_name': 'North Carolina',
            'state_code': 'NC',
            'district_id': 1,
            'district_name': 'district_1',
            'school_id': 2,
            'school_name': 'school_2',
            'school_category': 'High School',
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        institution_hierarchy = generate_institution_hierarchy(**params)
        self.assertEquals(institution_hierarchy.state_name, params['state_name'])
        self.assertEquals(institution_hierarchy.state_code, params['state_code'])
        self.assertEquals(institution_hierarchy.district_id, params['district_id'])
        self.assertEquals(institution_hierarchy.district_name, params['district_name'])
        self.assertEquals(institution_hierarchy.school_id, params['school_id'])
        self.assertEquals(institution_hierarchy.school_name, params['school_name'])
        self.assertEquals(institution_hierarchy.school_category, params['school_category'])
        self.assertEquals(institution_hierarchy.from_date, params['from_date'])
        self.assertEquals(institution_hierarchy.most_recent, params['most_recent'])
        self.assertIsInstance(institution_hierarchy.inst_hier_rec_id, int)

    def test_generate_student(self):
        params = {
            'section_guid': 1,
            'grade': 9,
            'state_code': 'NC',
            'district_id': 2,
            'school_id': 3,
            'school_name': 'school_2',
            'street_names': ['Suffolk', 'President', 'Allen'],
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        student = generate_student(**params)
        self.assertIsInstance(student.student_rec_id, int)
        self.assertIsInstance(student.student_id, UUID)
        self.assertIsInstance(student.first_name, str)
        self.assertIsInstance(student.last_name, str)
        address_component_words = student.address_1.split()
        address = int(address_component_words[0])
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
        self.assertEquals(student.district_id, params['district_id'])
        self.assertEquals(student.school_id, params['school_id'])
        self.assertIsInstance(student.from_date, date)
        self.assertIsInstance(student.most_recent, bool)

    def test_generate_students(self):
        params = {
            'number_of_students': 5,
            'section_guid': uuid4(),
            'grade': 5,
            'state_code': 'NC',
            'district_id': uuid4(),
            'school_id': uuid4(),
            'school_name': 'P.S. 118',
            'street_names': ['Vine, Main, Park'],
            'from_date': date(2013, 4, 23),
            'most_recent': True
        }
        students = generate_students(**params)
        self.assertEquals(len(students), params['number_of_students'])
        for student in students:
            self.assertIsInstance(student, Student)

    def test_generate_section(self):
        params = {
            'subject_name': 'ELA',
            'grade': 9,
            'state_code': 'NC',
            'district_id': 1,
            'school_id': 2,
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

    def test_generate_sections(self):
        params = {
            'number_of_sections': 9,
            'subject_name': 'ELA',
            'grade': 9,
            'state_code': 'NC',
            'district_id': uuid4(),
            'school_id': uuid4(),
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        sections = generate_sections(**params)
        self.assertEquals(len(sections), params['number_of_sections'])
        for section in sections:
            self.assertIsInstance(section, Section)

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
            'claim_cut_point_1': 1600,
            'claim_cut_point_2': 2000,
        }
        a = generate_assessment(**params)
        self.assertIsInstance(a.asmt_rec_id, int)
        self.assertIsInstance(a.asmt_guid, UUID)
        self.assertEquals(a.asmt_type, params['asmt_type'])

    def test_generate_assessments(self):
        params = {
            'grades': [9, 10, 11],
            'cut_points': [1400, 1800, 2100],
            'from_date': date(2013, 4, 23),
            'most_recent': True,
            'claim_cut_points': [1600, 2000]
        }
        assessments = generate_assessments(**params)
        for assessment in assessments:
            self.assertIsInstance(assessment, Assessment)

    def test_generate_staff(self):
        params = {
            'hier_user_type': 'Staff',
            'state_code': 'NC',
            'district_id': 1,
            'school_id': 2,
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
        self.assertEquals(staff.district_id, params['district_id'])
        self.assertEquals(staff.school_id, params['school_id'])
        self.assertIsInstance(staff.from_date, date)
        self.assertIsInstance(staff.most_recent, bool)

    def test_generate_multiple_staff(self):
        params = {
            'number_of_staff': 8,
            'hier_user_type': 'Teacher',
            'state_code': 'NC',
            'district_id': uuid4(),
            'school_id': uuid4(),
            'section_guid': uuid4(),
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        staff = generate_multiple_staff(**params)
        self.assertEquals(len(staff), params['number_of_staff'])
        for staff_member in staff:
            self.assertIsInstance(staff_member, Staff)


class DummyClass:
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

#     def test_generate_fact_assessment_outcome(self):
#         params = {
#             'asmt_rec_id': 10,
#             'student_id': uuid4(),
#             'teacher_guid': uuid4(),
#             'state_code': 'NC',
#             'district_id': uuid4(),
#             'school_id': uuid4(),
#             'section_guid': uuid4(),
#             'inst_hier_rec_id': 9,
#             'section_rec_id': 13,
#             'where_taken_id': 27,
#             'where_taken_name': 'P.S. 118',
#             'asmt_grade': 7,
#             'enrl_grade': 7,
#             'date_taken': date(2013, 4, 23),
#             'date_taken_day': 23,
#             'date_taken_month': 4,
#             'date_taken_year': 2013,
#             'asmt_score': 1750,
#             'asmt_score_range_min': 1650,
#             'asmt_score_range_max': 1850,
#             'asmt_perf_lvl': 1,
#             'asmt_claim_1_score': 1800,
#             'asmt_claim_1_score_range_min': 1700,
#             'asmt_claim_1_score_range_max': 1900,
#             'asmt_claim_2_score': 1600,
#             'asmt_claim_2_score_range_min': 1500,
#             'asmt_claim_2_score_range_max': 1700,
#             'asmt_claim_3_score': 1790,
#             'asmt_claim_3_score_range_min': 1690,
#             'asmt_claim_3_score_range_max': 1890,
#             'asmt_claim_4_score': 1729,
#             'asmt_claim_4_score_range_min': 1629,
#             'asmt_claim_4_score_range_max': 1829,
#             'batch_guid': '00000000-0000-0000-0000-000000000000',
#             'amst_year': 2012,
#             'asmt_type': 'SUMMATIVE',
#             'asmt_subject': 'Math',
#             'gender': 'male'
#         }
#         assessment_outcome = generate_fact_assessment_outcome(**params)
#         self.assertIsInstance(assessment_outcome, AssessmentOutcome)
#         for key, value in params.items():
#             self.assertEquals(getattr(assessment_outcome, key), value)

#     def test_generate_fact_assessment_outcomes(self):
#         section_guid = uuid4()
#         grade = 10
#         state_code = 'NC'
#         district_id = uuid4()
#         school_id = uuid4()
#         from_date = date(2013, 4, 23)
#         most_recent = True
#         student_1 = Student(100, uuid4(), 'Seth', 'Wimberly', '55 Washington St', 'Brooklyn', 11215,
#                             'Male', 'swimbery@swimberly.com', date(1988, 1, 1),
#                             section_guid, grade, state_code, district_id, school_id, from_date, most_recent)
#         student_2 = Student(100, uuid4(), 'Scott', 'MacGibbon', '65 Washington St', 'Brooklyn', 11215,
#                             'Male', 'smacgibbon@smacgibbon.com', date(1988, 3, 3),
#                             section_guid, grade, state_code, district_id, school_id, from_date, most_recent)
#         students = [student_1, student_2]
#
#         claim_score_1_a = ClaimScore(1800, 1700, 1900)
#         claim_score_1_b = ClaimScore(1900, 1800, 2000)
#         claim_score_1_c = ClaimScore(2000, 1900, 2100)
#         claim_scores_1 = [claim_score_1_a, claim_score_1_b, claim_score_1_c]
#         score_1 = AssessmentScore(1900, 3, 1800, 1900, claim_scores_1, date(2013, 4, 23))
#
#         claim_score_2_a = ClaimScore(1900, 1800, 2000)
#         claim_score_2_b = ClaimScore(2100, 2000, 2200)
#         claim_score_2_c = ClaimScore(2000, 1900, 2100)
#         claim_scores_2 = [claim_score_2_a, claim_score_2_b, claim_score_2_c]
#         score_2 = AssessmentScore(2000, 3, 1900, 2100, claim_scores_2, date(2013, 4, 23))
#
#         scores = [score_1, score_2]
#         teacher_guid = uuid4()
#         params = {
#             'students': students,
#             'scores': scores,
#             'asmt_rec_id': 111,
#             'teacher_guid': teacher_guid,
#             'state_code': state_code,
#             'district_id': district_id,
#             'school_id': school_id,
#             'section_guid': section_guid,
#             'inst_hier_rec_id': 200,
#             'section_rec_id': 300,
#             'where_taken_id': school_id,
#             'where_taken_name': 'P.S. 118',
#             'asmt_grade': 10,
#             'enrl_grade': 10,
#             'date_taken': date(2013, 4, 23),
#             'date_taken_day': 23,
#             'date_taken_month': 4,
#             'date_taken_year': 2013,
#             'batch_guid': '00000000-0000-0000-0000-000000000000'
#         }
#
#         assessment_outcomes = generate_fact_assessment_outcomes(**params)
#         self.assertEquals(len(assessment_outcomes), len(students))
#         for assessment_outcome in assessment_outcomes:
#             self.assertIsInstance(assessment_outcome, AssessmentOutcome)
