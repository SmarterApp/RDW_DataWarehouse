from uuid import uuid4

from idgen import IdGen
import util
from constants import DATAFILE_PATH, SCORE_MIN_MAX_RANGE


class InstitutionHierarchy:
    '''
    Institution Hierarchy object
    '''

    def __init__(self, number_of_students, student_teacher_ratio, low_grade, high_grade,
                 state_name, state_code, district_id, district_name, school_id, school_name, school_category, from_date, most_recent, row_id=None, to_date=None):
        '''
        Constructor
        '''
        self.number_of_students = number_of_students
        self.student_teacher_ratio = student_teacher_ratio
        self.low_grade = low_grade
        self.high_grade = high_grade

        # Ids can either be given to the constructor or provided by constructor
        # Either way, the row_id field must have a value
        id_generator = IdGen()
        if row_id is None:
            self.row_id = id_generator.get_id()
        else:
            self.row_id = row_id

        self.state_name = state_name
        self.state_code = state_code
        self.district_id = district_id
        self.district_name = district_name
        self.school_id = school_id
        self.school_name = school_name
        self.school_category = school_category
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

    def getRow(self):
        return [self.row_id, self.state_name, self.state_code, self.district_id, self.district_name, self.school_id, self.school_name, self.school_category, self.from_date, self.to_date, self.most_recent]

    # TODO: For all these getHeader methods, there must be a better way to return a list of the fields (in a defined order)
    # hard coding probably is not the best approach
    @classmethod
    def getHeader(cls):
        return ['row_id', 'state_name', 'state_code', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', 'from_date', 'to_date', 'most_recent']


class SectionSubject:
    '''
    SectionSubject Object
    '''

    def __init__(self, section_id, section_name, grade, class_name, subject_name, state_code, district_id, school_id, from_date, most_recent, to_date=None, row_id=None):

        # Ids can either be given to the constructor or provided by constructor
        # Either way, the row_id field must have a value
        id_generator = IdGen()
        if row_id is None:
            self.row_id = id_generator.get_id()
        else:
            self.row_id = row_id

        self.section_id = section_id
        self.section_name = section_name
        self.grade = grade
        self.class_name = class_name
        self.subject_name = subject_name
        self.state_code = state_code
        self.district_id = district_id
        self.school_id = school_id
        self.from_date = from_date
        self.most_recent = most_recent
        self.to_date = to_date

    def getRow(self):
        return [self.row_id, self.section_id, self.section_name, self.grade, self.class_name, self.subject_name, self.state_code, self.district_id, self.school_id, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['row_id', 'section_id', 'section_name', 'grade', 'class_name', 'subject_name', 'state_code', 'district_id', 'school_id', 'from_date', 'to_date', 'most_recent']


class Assessment:
    '''
    AssessmentType Object
    '''

    def __init__(self, asmt_id, asmt_external_id, asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_grade, asmt_subject, from_date, claim_1=None, claim_2=None, claim_3=None, claim_4=None, asmt_score_min=None, asmt_score_max=None,
                 asmt_perf_lvl_name_1=None, asmt_perf_lvl_name_2=None, asmt_perf_lvl_name_3=None, asmt_perf_lvl_name_4=None, asmt_perf_lvl_name_5=None, asmt_cut_point_1=None, asmt_cut_point_2=None, asmt_cut_point_3=None, asmt_cut_point_4=None,
                 asmt_custom_metadata=None, to_date=None, most_recent=None):
        '''
        Constructor
        '''
        self.asmt_id = asmt_id
        self.asmt_external_id = asmt_external_id
        self.asmt_type = asmt_type
        self.asmt_period = asmt_period
        self.asmt_period_year = asmt_period_year
        self.asmt_version = asmt_version
        self.asmt_grade = asmt_grade
        self.asmt_subject = asmt_subject

        self.claim_1 = claim_1
        self.claim_2 = claim_2
        self.claim_3 = claim_3
        self.claim_4 = claim_4

        self.asmt_perf_lvl_name_1 = asmt_perf_lvl_name_1
        self.asmt_perf_lvl_name_2 = asmt_perf_lvl_name_2
        self.asmt_perf_lvl_name_3 = asmt_perf_lvl_name_3
        self.asmt_perf_lvl_name_4 = asmt_perf_lvl_name_4
        self.asmt_perf_lvl_name_5 = asmt_perf_lvl_name_5
        self.asmt_score_min = asmt_score_min
        self.asmt_score_max = asmt_score_max

        self.asmt_cut_point_1 = asmt_cut_point_1
        self.asmt_cut_point_2 = asmt_cut_point_2
        self.asmt_cut_point_3 = asmt_cut_point_3
        self.asmt_cut_point_4 = asmt_cut_point_4

        self.asmt_custom_metadata = asmt_custom_metadata
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

    def __str__(self):
        '''
        toString Method
        '''

        return ("Assessment:[asmt_type: %s, subject: %s, asmt_type: %s, period: %s, version: %s, grade: %s]" % (self.asmt_type, self.asmt_subject, self.asmt_type, self.asmt_period, self.asmt_version, self.asmt_grade))

    def getRow(self):
        return [self.asmt_id, self.asmt_type, self.asmt_period, self.asmt_period_year, self.asmt_version, self.asmt_grade, self.asmt_subject,
                self.claim_1.claim_name, self.claim_2.claim_name, self.claim_3.claim_name, self.claim_4.claim_name if self.claim_4 is not None else '',
                self.asmt_perf_lvl_name_1, self.asmt_perf_lvl_name_2, self.asmt_perf_lvl_name_3, self.asmt_perf_lvl_name_4, self.asmt_perf_lvl_name_5,
                self.asmt_score_min, self.asmt_score_max,
                self.claim_1.claim_score_min, self.claim_1.claim_score_max, self.claim_2.claim_score_min, self.claim_2.claim_score_max,
                self.claim_3.claim_score_min, self.claim_3.claim_score_max,
                self.claim_4.claim_score_min if self.claim_4 is not None else '', self.claim_4.claim_score_max if self.claim_4 is not None else '',
                self.asmt_cut_point_1, self.asmt_cut_point_2, self.asmt_cut_point_3, self.asmt_cut_point_4,
                self.asmt_custom_metadata, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['asmt_id', 'asmt_type', 'asmt_period', 'asmt_period_year', 'asmt_version', 'asmt_grade', 'asmt_subject',
                'asmt_claim_1_name', 'asmt_claim_2_name', 'asmt_claim_3_name', 'asmt_claim_4_name',
                'asmt_perf_lvl_name_1', 'asmt_perf_lvl_name_2', 'asmt_perf_lvl_name_3', 'asmt_perf_lvl_name_4', 'asmt_perf_lvl_name_5',
                'asmt_score_min', 'asmt_score_max',
                'asmt_claim_1_score_min', 'asmt_claim_1_score_max', 'asmt_claim_2_score_min', 'asmt_claim_2_score_max',
                'asmt_claim_3_score_min', 'asmt_claim_3_score_max', 'asmt_claim_4_score_min', 'asmt_claim_4_score_max',
                'asmt_cut_point_1', 'asmt_cut_point_2', 'asmt_cut_point_3', 'asmt_cut_point_4',
                'asmt_custom_metadata', 'from_date', 'to_date', 'most_recent']


class AssessmentOutcome(object):
    '''
    Assessment outcome object
    '''

    def __init__(self, asmnt_outcome_id, asmnt_outcome_external_id, assessment, student, inst_hier_id, where_taken, date_taken, asmt_score, asmt_create_date, most_recent):
        self.asmnt_outcome_id = asmnt_outcome_id
        self.asmnt_outcome_external_id = asmnt_outcome_external_id
        self.assessment = assessment
        self.student = student
        self.inst_hier_id = inst_hier_id
        self.where_taken = where_taken
        self.date_taken = date_taken
        self.asmt_score = asmt_score
        self.asmt_create_date = asmt_create_date
        self.most_recent = most_recent

    def calc_perf_lvl(self, score, asmt):
        '''
        calculates a performance level as an integer based on a students overall score and
        the cutoffs for the assessment (0, 1 or 2)
        score -- a score object
        asmt -- an assessment object
        '''
        if score.overall > asmt.asmt_cut_point_3:
            if asmt.asmt_cut_point_4:
                return 4
            else:
                return 3
        elif score.overall > asmt.asmt_cut_point_2:
            return 2
        else:
            return 1

    def getRow(self):
        claims = self.asmt_score.claims

        asmt_perf_lvl = self.calc_perf_lvl(self.asmt_score, self.assessment)

        return [self.asmnt_outcome_id, self.asmnt_outcome_external_id, self.assessment.asmt_id,
                self.student.student_id, self.student.teacher_id, self.student.state_code,
                self.student.district_id, self.student.school_id, self.student.section_id,
                self.inst_hier_id, self.student.section_subject_id,
                self.where_taken.where_taken_id, self.where_taken.where_taken_name, self.assessment.asmt_grade, self.student.grade,
                self.date_taken.strftime('%Y%m%d'), self.date_taken.day, self.date_taken.month, self.date_taken.year,
                self.asmt_score.overall, max(0, self.asmt_score.overall - SCORE_MIN_MAX_RANGE), self.asmt_score.overall + SCORE_MIN_MAX_RANGE,
                asmt_perf_lvl,
                claims[0], max(0, claims[0] - SCORE_MIN_MAX_RANGE), claims[0] + SCORE_MIN_MAX_RANGE,
                claims[1], max(0, claims[1] - SCORE_MIN_MAX_RANGE), claims[1] + SCORE_MIN_MAX_RANGE,
                claims[2], max(0, claims[2] - SCORE_MIN_MAX_RANGE), claims[2] + SCORE_MIN_MAX_RANGE,
                claims[3] if len(claims) >= 4 else '', (max(0, claims[3] - SCORE_MIN_MAX_RANGE)) if len(claims) >= 4 else '',
                (claims[3] + SCORE_MIN_MAX_RANGE) if len(claims) >= 4 else '',
                self.asmt_create_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['asmnt_outcome_id', 'asmnt_outcome_external_id', 'asmt_id',
                'student_id', 'teacher_id', 'state_code',
                'district_id', 'school_id', 'section_id',
                'inst_hier_id', 'section_subject_id',
                'where_taken_id', 'where_taken_name', 'asmt_grade', 'enrl_grade',
                'date_taken', 'date_taken_day', 'date_taken_month', 'date_taken_year',
                'asmt_score', 'asmt_score_range_min', 'asmt_score_range_max', 'asmt_perf_lvl',
                'asmt_claim_1_score', 'asmt_claim_1_score_range_min', 'asmt_claim_1_score_range_max',
                'asmt_claim_2_score', 'asmt_claim_2_score_range_min', 'asmt_claim_2_score_range_max',
                'asmt_claim_3_score', 'asmt_claim_3_score_range_min', 'asmt_claim_3_score_range_max',
                'asmt_claim_4_score', 'asmt_claim_4_score_range_min', 'asmt_claim_4_score_range_max',
                'asmt_create_date', 'most_recent']


class Person(object):
    '''
    Base class for teacher, parent, student
    Right now, it only handles name fields
    '''

    def __init__(self, first_name, last_name, middle_name=None):
        '''
        Constructor
        if email and dob are not specified they are set to dummy values
        '''
        self.first_name = first_name.title()
        self.middle_name = middle_name.title() if middle_name is not None else middle_name
        self.last_name = last_name.title()


class Staff(Person):

    def __init__(self, first_name, last_name, section_id, hier_user_type, state_code, district_id, school_id, from_date, to_date=None, most_recent=None, middle_name=None, staff_id=None, staff_external_id=None):
        super().__init__(first_name, last_name, middle_name=middle_name)
        idgen = IdGen()
        self.row_id = idgen.get_id()
        if(staff_id):
            self.staff_id = staff_id
        else:
            self.staff_id = idgen.get_id()
        if(staff_external_id):
            self.staff_external_id = staff_external_id
        else:
            self.staff_external_id = uuid4()
        self.section_id = section_id
        self.hier_user_type = hier_user_type
        self.state_code = state_code
        self.district_id = district_id
        self.school_id = school_id
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

    def getRow(self):
        return [self.row_id, self.staff_id, self.staff_external_id, self.first_name, self.middle_name, self.last_name, self.section_id, self.hier_user_type, self.state_code, self.district_id, self.school_id, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['row_id', 'staff_id', 'staff_external_id', 'first_name', 'middle_name', 'last_name', 'section_id', 'hier_user_type', 'state_code', 'district_id', 'school_id', 'from_date', 'to_date', 'most_recent']


class ExternalUserStudent():
    '''
    ExternalUserStudent Object
    Corresponds to dim_external_user_student table
    '''

    def __init__(self, external_user_student_id, external_user_id, student_id, rel_start_date, rel_end_date=None):

        # Ids can either be given to the constructor or provided by constructor
        # Either way, both Id fields must have a value
        id_generator = IdGen()
        if external_user_student_id is None:
            self.external_user_student_id = id_generator.get_id()
        else:
            self.external_user_student_id = external_user_student_id
        if external_user_id is None:
            self.external_user_id = uuid4()
        else:
            self.external_user_id = external_user_id

        self.student_id = student_id
        self.rel_start_date = rel_start_date
        self.rel_end_date = rel_end_date

    def getRow(self):
        return [self.external_user_student_id, self.external_user_id, self.student_id, self.rel_start_date, self.rel_end_date]

    @classmethod
    def getHeader(cls):
        return ['external_user_student_id', 'external_user_id', 'student_id', 'from_date', 'to_date']


# For now, maps to dim_student
class StudentSection():

    def __init__(self, student, section_id, grade, from_date=None, to_date=None, most_recent=None, teacher_id=None, section_subject_id=None):
        idgen = IdGen()
        self.row_id = idgen.get_id()

        self.student_id = student.student_id
        self.first_name = student.first_name
        self.middle_name = student.middle_name
        self.last_name = student.last_name
        self.address_1 = student.address_1
        self.address_2 = student.address_2
        self.city = student.city
        self.zip_code = student.zip_code
        self.gender = student.gender
        self.email = student.email
        self.dob = util.generate_dob(grade)
        self.section_id = section_id
        self.grade = grade
        self.state_code = student.state_code
        self.district_id = student.district_id
        self.school_id = student.school_id
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

        self.teacher_id = teacher_id
        self.section_subject_id = section_subject_id

    def getRow(self):
        return [self.row_id, self.student_id, self.first_name, self.middle_name, self.last_name, self.address_1, self.address_2,
                self.city, self.zip_code, self.gender, self.email, self.dob, self.section_id, self.grade,
                self.state_code, self.district_id, self.school_id, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['row_id', 'student_id', 'first_name', 'middle_name', 'last_name', 'address_1', 'address_2',
                'city', 'zip_code', 'gender', 'email', 'dob', 'section_id', 'grade',
                'state_code', 'district_id', 'school_id', 'from_date', 'to_date', 'most_recent']
