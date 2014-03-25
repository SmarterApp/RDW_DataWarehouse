import unittest
import get_list_of_students
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, Index
from sqlalchemy import String, Boolean, SmallInteger, Float
from sqlalchemy.sql import Select, FromClause
from sqlalchemy.types import Text
from sqlalchemy import ForeignKey


class TestGetListOfStudents(unittest.TestCase):

    def setUp(self):
        self.parameters = {'schema': None,
                           'state_code': None,
                           'district_id': None,
                           'school_id': None,
                           'section_id': None,
                           'grade': None
                           }
        self.columns = ['student_id', 'teacher_id', 'state_code', 'district_id', 'school_id', 'section_id', 'inst_hier_rec_id', 'section_rec_id', 'enrl_grade', 'school_name', 'subject_name']

    def test_prepare_query_noOptionalParameters(self):
        schema_name = 'test_schema'
        self.parameters['schema'] = schema_name
        metadata = generate_ed_metadata(self.parameters['schema'])
        query = get_list_of_students.prepare_query(self.parameters['schema'], metadata, self.parameters)

        # query is a Select object
        self.assertIsInstance(query, Select)

        # verify selected columns
        self.assertEqual(len(query.columns), len(self.columns))
        i = 0
        for col in query.columns:
            self.assertIsInstance(col, Column)
            self.assertEqual(str(col), self.columns[i])
            i += 1

        # verify FromClause
        self.assertEqual(len(query.froms), 1)
        from_obj = (query.froms)[0]
        self.assertIsInstance(from_obj, FromClause)
        self.assertEqual(str(from_obj).lower(), make_expected_from_clause(schema_name))

        # verify there is no where clause
        self.assertFalse('where'.lower() in str(query).lower())

    def test_prepare_query_hasAllOptionalParameters(self):
        schema_name = 'test_schema'
        self.parameters['schema'] = schema_name
        self.parameters['state_code'] = 'DE'
        self.parameters['district_id'] = '123'
        self.parameters['school_id'] = '298'
        self.parameters['section_id'] = '98124'
        self.parameters['grade'] = '1'

        metadata = generate_ed_metadata(self.parameters['schema'])
        query = get_list_of_students.prepare_query(self.parameters['schema'], metadata, self.parameters)

        # query is a Select object
        self.assertIsInstance(query, Select)

        # verify selected columns
        self.assertEqual(len(query.columns), len(self.columns))
        i = 0
        for col in query.columns:
            self.assertIsInstance(col, Column)
            self.assertEqual(str(col), self.columns[i])
            i += 1

        # verify FromClause
        self.assertEqual(len(query.froms), 1)
        from_obj = (query.froms)[0]
        self.assertIsInstance(from_obj, FromClause)
        self.assertEqual(str(from_obj).lower(), make_expected_from_clause(schema_name))

        # verify where clause
        self.assertTrue('where'.lower() in str(query).lower())
        index_of_where = str(query).lower().index('where')
        actual_where_clause = str(query).lower()[index_of_where:]
        self.assertEqual(actual_where_clause, make_expected_where_clause(schema_name))


def make_expected_from_clause(schema_name):
    return (schema_name + '.dim_student JOIN ' + schema_name + '.dim_section_subject ON ' + schema_name +
            '.dim_student.section_id = ' + schema_name + '.dim_section_subject.section_id JOIN ' + schema_name +
            '.dim_staff ON ' + schema_name + '.dim_student.section_id = ' + schema_name +
            '.dim_staff.section_id JOIN ' + schema_name + '.dim_inst_hier ON ' + schema_name +
            '.dim_student.school_id = ' + schema_name + '.dim_inst_hier.school_id').lower()


def make_expected_where_clause(schema_name):
    return ('WHERE ' + schema_name + '.dim_student.state_code = :state_code_1 AND ' + schema_name + '.dim_student.district_id = :district_id_1 AND ' +
            schema_name + '.dim_student.school_id = :school_id_1 AND ' + schema_name + '.dim_student.section_id = :section_id_1 AND ' +
            schema_name + '.dim_student.grade = :grade_1').lower()


def generate_ed_metadata(schema_name=None, bind=None):
    '''
    This function is the copy of /edware/blob/master/edschema/edschema/ed_metadata.py
    Need to be replaced by importing from the above file if possible
    '''

    metadata = MetaData(schema=schema_name, bind=bind)

    # Two-letter state - some countries have 3 or more, but two will do for US
    instit_hier = Table('dim_inst_hier', metadata,
                        Column('inst_hier_rec_id', String(50), primary_key=True),
                        Column('state_name', String(32), nullable=False),
                        Column('state_code', String(2), nullable=False),
                        Column('district_id', String(50), nullable=False),
                        Column('district_name', String(256), nullable=False),
                        Column('school_id', String(50), nullable=False),
                        Column('school_name', String(256), nullable=False),
                        Column('school_category', String(20), nullable=False),
                        Column('from_date', String(8), nullable=False),
                        Column('to_date', String(8), nullable=True),
                        Column('most_recent', Boolean),
                        )

    Index('dim_inst_hier_idx', instit_hier.c.inst_hier_rec_id, unique=True)
    Index('dim_inst_hier_codex', instit_hier.c.state_code, instit_hier.c.district_id, instit_hier.c.school_id, unique=False)

    sections = Table('dim_section_subject', metadata,
                     Column('section_rec_id', String(50), primary_key=True),
                     Column('section_id', String(50), nullable=False),
                     Column('section_name', String(256), nullable=False),
                     Column('grade', String(10), nullable=False),
                     Column('class_name', String(256), nullable=False),
                     Column('subject_name', String(256), nullable=False),
                     Column('state_code', String(2), nullable=False),
                     Column('district_id', String(50), nullable=False),
                     Column('school_id', String(50), nullable=False),
                     Column('from_date', String(8), nullable=False),
                     Column('to_date', String(8), nullable=True),
                     Column('most_recent', Boolean),
                     )

    Index('dim_section_idx', sections.c.section_rec_id, unique=True)
    Index('dim_section_current_idx', sections.c.section_id, sections.c.subject_name, sections.c.grade, sections.c.most_recent, unique=False)
    Index('dim_section_dim_inst_hier_idx', sections.c.state_code, sections.c.district_id, sections.c.school_id, sections.c.from_date, sections.c.to_date, unique=False)

    # NB! Figure out uniques in dim_student
    students = Table('dim_student', metadata,
                     Column('student_rec_id', String(50), primary_key=True),
                     Column('student_id', String(50), nullable=False),
                     Column('first_name', String(256), nullable=False),
                     Column('middle_name', String(256), nullable=True),
                     Column('last_name', String(256), nullable=False),
                     Column('address_1', String(256), nullable=False),
                     Column('address_2', String(256), nullable=True),
                     Column('city', String(100), nullable=False),
                     Column('zip_code', String(5), nullable=False),
                     Column('gender', String(10), nullable=False),
                     Column('email', String(256), nullable=False),
                     Column('dob', String(8), nullable=False),
                     Column('section_id', String(50), nullable=False),
                     Column('grade', String(10), nullable=False),
                     Column('state_code', String(2), nullable=False),
                     Column('district_id', String(50), nullable=False),
                     Column('school_id', String(50), nullable=False),
                     Column('from_date', String(8), nullable=False),
                     Column('to_date', String(8), nullable=True),
                     Column('most_recent', Boolean),
                     )

    Index('dim_student_idx', students.c.student_id, students.c.most_recent, unique=False)
    Index('dim_student_dim_inst_hier_idx',
          students.c.state_code, students.c.district_id, students.c.school_id, students.c.section_id, students.c.grade,
          students.c.from_date, students.c.to_date, unique=False)

    external_user_student = Table('external_user_student_rel', metadata,
                                  Column('external_user_student_id', String(50), primary_key=True),
                                  Column('external_user_id', String(256), nullable=False),
                                  Column('student_id', String(50), nullable=False),  # NB! Figure out uniques in dim_student
                                  Column('from_date', String(8), nullable=False),
                                  Column('to_date', String(8), nullable=True),
                                  )

    Index('dim_external_user_student_idx', external_user_student.c.external_user_student_id, unique=True)
    Index('dim_external_user_student_student_x', external_user_student.c.external_user_id, external_user_student.c.student_id, unique=True)

    staff = Table('dim_staff', metadata,
                  Column('staff_rec_id', String(50), primary_key=True),
                  Column('staff_id', String(50), nullable=False),
                  Column('first_name', String(256), nullable=False),
                  Column('middle_name', String(256), nullable=True),
                  Column('last_name', String(256), nullable=False),
                  Column('section_id', String(50), nullable=False),
                  Column('hier_user_type', String(10), nullable=False),
                  Column('state_code', String(2), nullable=False),
                  Column('district_id', String(50), nullable=False),
                  Column('school_id', String(50), nullable=False),
                  Column('from_date', String(8), nullable=False),
                  Column('to_date', String(8), nullable=True),
                  Column('most_recent', Boolean),
                  )

    Index('dim_staff_idx', staff.c.staff_rec_id, unique=True)
    Index('dim_staff_id_currentx', staff.c.staff_id, staff.c.most_recent, unique=False)
    Index('dim_staff_dim_inst_hier_idx', staff.c.state_code, staff.c.district_id, staff.c.school_id, staff.c.from_date, staff.c.to_date, unique=False)

    assessment = Table('dim_asmt', metadata,
                       Column('asmt_rec_id', String(50), primary_key=True),
                       Column('asmt_id', String(50), nullable=False),
                       Column('asmt_type', String(16), nullable=False),
                       Column('asmt_period', String(32), nullable=False),
                       Column('asmt_period_year', SmallInteger, nullable=False),
                       Column('asmt_version', String(16), nullable=False),
                       Column('asmt_subject', String(100)),
                       Column('asmt_claim_1_name', String(256), nullable=True),
                       Column('asmt_claim_2_name', String(256), nullable=True),
                       Column('asmt_claim_3_name', String(256), nullable=True),
                       Column('asmt_claim_4_name', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_1', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_2', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_3', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_4', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_5', String(256), nullable=True),
                       Column('asmt_score_min', SmallInteger, nullable=True),
                       Column('asmt_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_1_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_1_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_1_score_weight', Float, nullable=True),
                       Column('asmt_claim_2_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_2_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_2_score_weight', Float, nullable=True),
                       Column('asmt_claim_3_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_3_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_3_score_weight', Float, nullable=True),
                       Column('asmt_claim_4_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_4_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_4_score_weight', Float, nullable=True),
                       Column('asmt_cut_point_1', SmallInteger, nullable=True),
                       Column('asmt_cut_point_2', SmallInteger, nullable=True),
                       Column('asmt_cut_point_3', SmallInteger, nullable=True),
                       Column('asmt_cut_point_4', SmallInteger, nullable=True),
                       Column('asmt_custom_metadata', Text, nullable=True),
                       Column('from_date', String(8), nullable=False),
                       Column('to_date', String(8), nullable=True),
                       Column('most_recent', Boolean),
                       )

    Index('dim_asmt_rec_idx', assessment.c.asmt_rec_id, unique=True)
    Index('dim_asmt_idx', assessment.c.asmt_id, unique=False)

    assessment_outcome = Table('fact_asmt_outcome', metadata,
                               Column('asmnt_outcome_id', String(50), primary_key=True),
                               Column('asmnt_outcome_external_id', String(256), nullable=False),
                               Column('asmt_rec_id', None, ForeignKey(assessment.c.asmt_rec_id), nullable=False),
                               Column('student_id', String(50), nullable=False),
                               Column('teacher_id', String(50), nullable=False),
                               Column('state_code', String(2), nullable=False),
                               Column('district_id', String(50), nullable=False),
                               Column('school_id', String(50), nullable=False),
                               Column('section_id', String(50), nullable=False),
                               Column('inst_hier_rec_id', None, ForeignKey(instit_hier.c.inst_hier_rec_id), nullable=False),
                               Column('section_rec_id', None, ForeignKey(sections.c.section_rec_id), nullable=False),
                               Column('where_taken_id', String(50), nullable=True),  # external id if provided
                               Column('where_taken_name', String(256), primary_key=True),
                               Column('asmt_grade', String(10), nullable=False),
                               Column('enrl_grade', String(10), nullable=False),
                               Column('date_taken', String(8), nullable=False),
                               Column('date_taken_day', SmallInteger, nullable=False),
                               Column('date_taken_month', SmallInteger, nullable=False),
                               Column('date_taken_year', SmallInteger, nullable=False),
                               Column('asmt_score', SmallInteger, nullable=False),
                               Column('asmt_score_range_min', SmallInteger, nullable=False),
                               Column('asmt_score_range_max', SmallInteger, nullable=False),
                               Column('asmt_perf_lvl', SmallInteger, nullable=False),
                               Column('asmt_claim_1_score', SmallInteger, nullable=True),
                               Column('asmt_claim_1_score_range_min', SmallInteger, nullable=True),
                               Column('asmt_claim_1_score_range_max', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score_range_min', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score_range_max', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score_range_min', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score_range_max', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score_range_min', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score_range_max', SmallInteger, nullable=True),
                               Column('asmt_create_date', String(8), nullable=False),
                               Column('status', String(2), nullable=False),
                               Column('most_recent', Boolean),
                               )

    Index('fact_asmt_outcome_idx', assessment_outcome.c.asmnt_outcome_id, unique=True)

    return metadata
if __name__ == "__main__":
    unittest.main()
