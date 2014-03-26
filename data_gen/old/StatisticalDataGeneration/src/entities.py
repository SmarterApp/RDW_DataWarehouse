from uuid import uuid4

from idgen import IdGen
from constants import MAXIMUM_ASSESSMENT_SCORE, MINIMUM_ASSESSMENT_SCORE, AVERAGE_ASSESSMENT_SCORE, ASSESSMENT_SCORE_STANDARD_DEVIATION


class InstitutionHierarchy:
    '''
    Institution Hierarchy object
    '''

    def __init__(self, number_of_students, student_teacher_ratio, low_grade, high_grade,
                 state_name, state_code, district_guid, district_name, school_guid, school_name, school_category, from_date, most_recent, inst_hier_rec_id=None, to_date=None):
        '''
        Constructor
        '''
        self.number_of_students = number_of_students
        self.student_teacher_ratio = student_teacher_ratio
        self.low_grade = low_grade
        self.high_grade = high_grade

        # Ids can either be given to the constructor or provided by constructor
        # Either way, the inst_hier_rec_id field must have a value
        id_generator = IdGen()
        if inst_hier_rec_id is None:
            self.inst_hier_rec_id = id_generator.get_id()
        else:
            self.inst_hier_rec_id = inst_hier_rec_id

        self.state_name = state_name
        self.state_code = state_code
        self.district_guid = district_guid
        self.district_name = district_name
        self.school_guid = school_guid
        self.school_name = school_name
        self.school_category = school_category
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

    def getRow(self):
        return [self.inst_hier_rec_id, self.state_name, self.state_code, self.district_guid, self.district_name, self.school_guid, self.school_name, self.school_category, self.from_date, self.to_date, self.most_recent]

    # TODO: For all these getHeader methods, there must be a better way to return a list of the fields (in a defined order)
    # hard coding probably is not the best approach
    @classmethod
    def getHeader(cls):
        return ['inst_hier_rec_id', 'state_name', 'state_code', 'district_guid', 'district_name', 'school_guid', 'school_name', 'school_category', 'from_date', 'to_date', 'most_recent']


class Section:
    '''
    Section Object
    '''
    def __init__(self, section_guid, section_name, grade, class_name, subject_name, state_code, district_guid, school_guid, from_date, most_recent, to_date=None, section_rec_id=None):

        # Ids can either be given to the constructor or provided by constructor
        # Either way, the section_rec_id field must have a value
        id_generator = IdGen()
        if section_rec_id is None:
            self.section_rec_id = id_generator.get_id()
        else:
            self.section_rec_id = section_rec_id

        self.section_guid = section_guid
        self.section_name = section_name
        self.grade = grade
        self.class_name = class_name
        self.subject_name = subject_name
        self.state_code = state_code
        self.district_guid = district_guid
        self.school_guid = school_guid
        self.from_date = from_date
        self.most_recent = most_recent
        self.to_date = to_date

    def getRow(self):
        return [self.section_rec_id, self.section_guid, self.section_name, self.grade, self.class_name, self.subject_name, self.state_code, self.district_guid, self.school_guid, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['section_rec_id', 'section_guid', 'section_name', 'grade', 'class_name', 'subject_name', 'state_code', 'district_guid', 'school_guid', 'from_date', 'to_date', 'most_recent']


class Assessment:
    '''
    Assessment Object
    '''
    def __init__(self, asmt_rec_id, asmt_guid, asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_grade, asmt_subject, from_date, claim_list, asmt_score_min=None, asmt_score_max=None,
                 asmt_perf_lvl_name_1=None, asmt_perf_lvl_name_2=None, asmt_perf_lvl_name_3=None, asmt_perf_lvl_name_4=None, asmt_perf_lvl_name_5=None, asmt_cut_point_1=None, asmt_cut_point_2=None, asmt_cut_point_3=None, asmt_cut_point_4=None,
                 asmt_custom_metadata=None, to_date=None, most_recent=None, minimum_assessment_score=MINIMUM_ASSESSMENT_SCORE, maximum_assessment_score=MAXIMUM_ASSESSMENT_SCORE, average_assessment_score=AVERAGE_ASSESSMENT_SCORE, assessment_score_standard_deviation=ASSESSMENT_SCORE_STANDARD_DEVIATION):
        '''
        Constructor
        '''
        self.asmt_guid = asmt_guid
        self.asmt_rec_id = asmt_rec_id
        self.asmt_type = asmt_type
        self.asmt_period = asmt_period
        self.asmt_period_year = asmt_period_year
        self.asmt_version = asmt_version
        self.asmt_grade = asmt_grade
        self.asmt_subject = asmt_subject

        # TODO: Make this more general. Hard coding acceptable length values doesn't seem ideal.
        # All assessments have either 3 or 4 claims
        if len(claim_list) == 3:
            self.claim_1 = claim_list[0]
            self.claim_2 = claim_list[1]
            self.claim_3 = claim_list[2]
            self.claim_4 = None
        elif len(claim_list) == 4:
            self.claim_1 = claim_list[0]
            self.claim_2 = claim_list[1]
            self.claim_3 = claim_list[2]
            self.claim_4 = claim_list[3]
        else:
            raise Exception('claim_list contains ' + str(len(claim_list)) + ' claims, but it should only contain 3 or 4 claims.')

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

        # These values are not output by get_row. They are only used to generate assessment_outcomes.
        self.average_score = average_assessment_score
        self.standard_deviation = assessment_score_standard_deviation
        self.score_minimum = minimum_assessment_score
        self.score_maximum = maximum_assessment_score

    def get_claim_list(self):
        claims = [self.claim_1, self.claim_2, self.claim_3]
        if self.claim_4:
            claims.append(self.claim_4)
        return claims

    def __str__(self):
        '''
        toString Method
        '''
        return ("Assessment:[asmt_type: %s, subject: %s, asmt_type: %s, period: %s, version: %s, grade: %s]" % (self.asmt_type, self.asmt_subject, self.asmt_type, self.asmt_period, self.asmt_version, self.asmt_grade))

    # TODO: set all fields in init function, not in getRow
    def getRow(self):
        return [self.asmt_rec_id, self.asmt_guid, self.asmt_type, self.asmt_period, self.asmt_period_year, self.asmt_version,
                self.asmt_subject, self.claim_1.claim_name, self.claim_2.claim_name, self.claim_3.claim_name,
                self.claim_4.claim_name if self.claim_4 is not None else '',
                self.asmt_perf_lvl_name_1, self.asmt_perf_lvl_name_2, self.asmt_perf_lvl_name_3,
                self.asmt_perf_lvl_name_4, self.asmt_perf_lvl_name_5,
                self.asmt_score_min, self.asmt_score_max,
                self.claim_1.claim_score_min, self.claim_1.claim_score_max, self.claim_1.claim_score_weight,
                self.claim_2.claim_score_min, self.claim_2.claim_score_max, self.claim_2.claim_score_weight,
                self.claim_3.claim_score_min, self.claim_3.claim_score_max, self.claim_3.claim_score_weight,
                self.claim_4.claim_score_min if self.claim_4 is not None else '', self.claim_4.claim_score_max if self.claim_4 is not None else '', self.claim_4.claim_score_weight if self.claim_4 is not None else 0,
                self.asmt_cut_point_1, self.asmt_cut_point_2, self.asmt_cut_point_3, self.asmt_cut_point_4,
                self.asmt_custom_metadata, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['asmt_rec_id', 'asmt_guid', 'asmt_type', 'asmt_period', 'asmt_period_year', 'asmt_version', 'asmt_subject',
                'asmt_claim_1_name', 'asmt_claim_2_name', 'asmt_claim_3_name', 'asmt_claim_4_name',
                'asmt_perf_lvl_name_1', 'asmt_perf_lvl_name_2', 'asmt_perf_lvl_name_3', 'asmt_perf_lvl_name_4', 'asmt_perf_lvl_name_5',
                'asmt_score_min', 'asmt_score_max',
                'asmt_claim_1_score_min', 'asmt_claim_1_score_max', 'asmt_claim_1_score_weight',
                'asmt_claim_2_score_min', 'asmt_claim_2_score_max', 'asmt_claim_2_score_weight',
                'asmt_claim_3_score_min', 'asmt_claim_3_score_max', 'asmt_claim_3_score_weight',
                'asmt_claim_4_score_min', 'asmt_claim_4_score_max', 'asmt_claim_4_score_weight',
                'asmt_cut_point_1', 'asmt_cut_point_2', 'asmt_cut_point_3', 'asmt_cut_point_4',
                'asmt_custom_metadata', 'from_date', 'to_date', 'most_recent']


class AssessmentOutcome(object):

    def __init__(self, asmnt_outcome_rec_id, asmt_rec_id, student_guid,
                 teacher_guid, state_code, district_guid, school_guid, section_guid, inst_hier_rec_id, section_rec_id,
                 where_taken_id, where_taken_name, asmt_grade, enrl_grade, date_taken, date_taken_day,
                 date_taken_month, date_taken_year,
                 asmt_score, asmt_score_range_min, asmt_score_range_max, asmt_perf_lvl,
                 asmt_claim_1_score, asmt_claim_1_score_range_min, asmt_claim_1_score_range_max,
                 asmt_claim_2_score, asmt_claim_2_score_range_min, asmt_claim_2_score_range_max,
                 asmt_claim_3_score, asmt_claim_3_score_range_min, asmt_claim_3_score_range_max,
                 asmt_claim_4_score, asmt_claim_4_score_range_min, asmt_claim_4_score_range_max,
                 asmt_create_date, status, most_recent):

        self.asmnt_outcome_rec_id = asmnt_outcome_rec_id
        self.asmt_rec_id = asmt_rec_id
        self.student_guid = student_guid
        self.teacher_guid = teacher_guid
        self.state_code = state_code
        self.district_guid = district_guid
        self.school_guid = school_guid
        self.section_guid = section_guid
        self.inst_hier_rec_id = inst_hier_rec_id
        self.section_rec_id = section_rec_id
        self.where_taken_id = where_taken_id
        self.where_taken_name = where_taken_name
        self.asmt_grade = asmt_grade
        self.enrl_grade = enrl_grade
        self.date_taken = date_taken
        self.date_taken_day = date_taken_day
        self.date_taken_month = date_taken_month
        self.date_taken_year = date_taken_year

        # Overall Assessment Data
        self.asmt_score = asmt_score
        self.asmt_score_range_min = asmt_score_range_min
        self.asmt_score_range_max = asmt_score_range_max
        self.asmt_perf_lvl = asmt_perf_lvl

        # Assessment Claim Data
        self.asmt_claim_1_score = asmt_claim_1_score
        self.asmt_claim_1_score_range_min = asmt_claim_1_score_range_min
        self.asmt_claim_1_score_range_max = asmt_claim_1_score_range_max
        self.asmt_claim_2_score = asmt_claim_2_score
        self.asmt_claim_2_score_range_min = asmt_claim_2_score_range_min
        self.asmt_claim_2_score_range_max = asmt_claim_2_score_range_max
        self.asmt_claim_3_score = asmt_claim_3_score
        self.asmt_claim_3_score_range_min = asmt_claim_3_score_range_min
        self.asmt_claim_3_score_range_max = asmt_claim_3_score_range_max

        # These fields may or may not be null (Some have a 4th claim, others don't)
        self.asmt_claim_4_score = asmt_claim_4_score
        self.asmt_claim_4_score_range_min = asmt_claim_4_score_range_min
        self.asmt_claim_4_score_range_max = asmt_claim_4_score_range_max

        self.asmt_create_date = asmt_create_date
        self.status = status
        self.most_recent = most_recent

    def getRow(self):
        return [self.asmnt_outcome_rec_id, self.asmt_rec_id,
                self.student_guid, self.teacher_guid, self.state_code,
                self.district_guid, self.school_guid, self.section_guid,
                self.inst_hier_rec_id, self.section_rec_id,
                self.where_taken_id, self.where_taken_name, self.asmt_grade, self.enrl_grade,
                self.date_taken, self.date_taken_day, self.date_taken_month, self.date_taken_year,
                self.asmt_score, self.asmt_score_range_min, self.asmt_score_range_max,
                self.asmt_perf_lvl,
                self.asmt_claim_1_score, self.asmt_claim_1_score_range_min, self.asmt_claim_1_score_range_max,
                self.asmt_claim_2_score, self.asmt_claim_2_score_range_min, self.asmt_claim_2_score_range_max,
                self.asmt_claim_3_score, self.asmt_claim_3_score_range_min, self.asmt_claim_3_score_range_max,
                self.asmt_claim_4_score, self.asmt_claim_4_score_range_min, self.asmt_claim_4_score_range_max,
                self.asmt_create_date, self.status, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['asmnt_outcome_rec_id', 'asmt_rec_id',
                'student_guid', 'teacher_guid', 'state_code',
                'district_guid', 'school_guid', 'section_guid',
                'inst_hier_rec_id', 'section_rec_id',
                'where_taken_id', 'where_taken_name', 'asmt_grade', 'enrl_grade',
                'date_taken', 'date_taken_day', 'date_taken_month', 'date_taken_year',
                'asmt_score', 'asmt_score_range_min', 'asmt_score_range_max', 'asmt_perf_lvl',
                'asmt_claim_1_score', 'asmt_claim_1_score_range_min', 'asmt_claim_1_score_range_max',
                'asmt_claim_2_score', 'asmt_claim_2_score_range_min', 'asmt_claim_2_score_range_max',
                'asmt_claim_3_score', 'asmt_claim_3_score_range_min', 'asmt_claim_3_score_range_max',
                'asmt_claim_4_score', 'asmt_claim_4_score_range_min', 'asmt_claim_4_score_range_max',
                'asmt_create_date', 'status', 'most_recent']


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

    def __init__(self, first_name, last_name, section_guid, hier_user_type, state_code, district_guid, school_guid, from_date, to_date=None, most_recent=None, middle_name=None, staff_guid=None):
        super().__init__(first_name, last_name, middle_name=middle_name)
        idgen = IdGen()
        self.staff_rec_id = idgen.get_id()
        if(staff_guid):
            self.staff_guid = staff_guid
        else:
            self.staff_guid = idgen.get_id()
        self.section_guid = section_guid
        self.hier_user_type = hier_user_type
        self.state_code = state_code
        self.district_guid = district_guid
        self.school_guid = school_guid
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

    def getRow(self):
        return [self.staff_rec_id, self.staff_guid, self.first_name, self.middle_name, self.last_name, self.section_guid, self.hier_user_type, self.state_code, self.district_guid, self.school_guid, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['staff_rec_id', 'staff_guid', 'first_name', 'middle_name', 'last_name', 'section_guid', 'hier_user_type', 'state_code', 'district_guid', 'school_guid', 'from_date', 'to_date', 'most_recent']


class ExternalUserStudent():
    '''
    ExternalUserStudent Object
    Corresponds to dim_external_user_student table
    '''

    def __init__(self, external_user_student_guid, external_user_guid, student_guid, rel_start_date, rel_end_date=None):

        # Ids can either be given to the constructor or provided by constructor
        # Either way, both Id fields must have a value
        id_generator = IdGen()
        if external_user_student_guid is None:
            self.external_user_student_guid = id_generator.get_id()
        else:
            self.external_user_student_guid = external_user_student_guid
        if external_user_guid is None:
            self.external_user_guid = uuid4()
        else:
            self.external_user_guid = external_user_guid

        self.student_guid = student_guid
        self.rel_start_date = rel_start_date
        self.rel_end_date = rel_end_date

    def getRow(self):
        return [self.external_user_student_guid, self.external_user_guid, self.student_guid, self.rel_start_date, self.rel_end_date]

    @classmethod
    def getHeader(cls):
        return ['external_user_student_guid', 'external_user_guid', 'student_guid', 'from_date', 'to_date']


class Student():
    '''
        Student Object maps to dim_student table

        StudentBioInfo contains most of the data used to create a Student object
        Student Objects hold additional information (section, grade, from_date, etc.)
    '''

    # TODO: This class shouldn't have to hold teacher_id or section_rec_id since dim_student doesn't
    # have this info. Think of a better way to pass this information.
    # For now, we use this class to hold this info for later injection into fao.
    def __init__(self, student_bio_info, section_guid, grade, from_date, most_recent, to_date=None, teacher_guid=None, section_rec_id=None):
        idgen = IdGen()
        self.student_rec_id = idgen.get_id()

        self.student_guid = student_bio_info.student_guid
        self.first_name = student_bio_info.first_name
        self.middle_name = student_bio_info.middle_name
        self.last_name = student_bio_info.last_name
        self.address_1 = student_bio_info.address_1
        self.address_2 = student_bio_info.address_2
        self.city = student_bio_info.city
        self.zip_code = student_bio_info.zip_code
        self.gender = student_bio_info.gender
        self.email = student_bio_info.email
        self.dob = student_bio_info.dob
        self.section_guid = section_guid
        self.grade = grade
        self.state_code = student_bio_info.state_code
        self.district_guid = student_bio_info.district_guid
        self.school_guid = student_bio_info.school_guid
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

        # TODO: get rid of me!
        self.teacher_guid = teacher_guid
        self.section_rec_id = section_rec_id

    def getRow(self):
        return [self.student_rec_id, self.student_guid, self.first_name, self.middle_name, self.last_name, self.address_1, self.address_2,
                self.city, self.zip_code, self.gender, self.email, self.dob, self.section_guid, self.grade,
                self.state_code, self.district_guid, self.school_guid, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['student_rec_id', 'student_guid', 'first_name', 'middle_name', 'last_name', 'address_1', 'address_2',
                'city', 'zip_code', 'gender', 'email', 'dob', 'section_guid', 'grade',
                'state_code', 'district_guid', 'school_guid', 'from_date', 'to_date', 'most_recent']
