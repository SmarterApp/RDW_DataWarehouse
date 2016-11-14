__author__ = 'abrien'


# TODO: get rid of camel-cased function names
class InstitutionHierarchy:
    '''
    Institution Hierarchy object
    '''

    def __init__(self, inst_hier_rec_id, state_name, state_code, district_id, district_name, school_id, school_name, school_category,
                 from_date, most_recent, to_date=None):

        self.inst_hier_rec_id = inst_hier_rec_id

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

        # Attributes that will not be written
        self.student_counts = {}

    def getRow(self):
        '''
        Returns the information stored in this object as csv row
        '''
        return [self.inst_hier_rec_id, self.state_name, self.state_code, self.district_id, self.district_name, self.school_id, self.school_name, self.school_category, self.from_date, self.to_date, self.most_recent]

    # TODO: For all these getHeader methods, there must be a better way to return a list of the fields (in a defined order)
    # hard coding probably is not the best approach
    @classmethod
    def getHeader(cls):
        '''
        Returns the csv of header of this entity
        '''
        return ['inst_hier_rec_id', 'state_name', 'state_code', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', 'from_date', 'to_date', 'most_recent']


class Section:
    '''
    Section Object
    '''
    def __init__(self, section_rec_id, section_guid, section_name, grade, class_name, subject_name, state_code, district_id, school_id, from_date, most_recent, to_date=None):

        self.section_rec_id = section_rec_id

        self.section_guid = section_guid
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
        return [self.section_rec_id, self.section_guid, self.section_name, self.grade, self.class_name, self.subject_name, self.state_code, self.district_id, self.school_id, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['section_rec_id', 'section_guid', 'section_name', 'grade', 'class_name', 'subject_name', 'state_code', 'district_id', 'school_id', 'from_date', 'to_date', 'most_recent']


class Assessment:
    '''
    Assessment Object
    '''
    def __init__(self, asmt_rec_id, asmt_guid, asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_subject,
                 asmt_grade, from_date, most_recent,
                 asmt_claim_1_name=None, asmt_claim_2_name=None, asmt_claim_3_name=None, asmt_claim_4_name=None,
                 asmt_perf_lvl_name_1=None, asmt_perf_lvl_name_2=None, asmt_perf_lvl_name_3=None, asmt_perf_lvl_name_4=None, asmt_perf_lvl_name_5=None,
                 asmt_score_min=None, asmt_score_max=None,
                 asmt_claim_1_score_min=None, asmt_claim_1_score_max=None, asmt_claim_1_score_weight=None,
                 asmt_claim_2_score_min=None, asmt_claim_2_score_max=None, asmt_claim_2_score_weight=None,
                 asmt_claim_3_score_min=None, asmt_claim_3_score_max=None, asmt_claim_3_score_weight=None,
                 asmt_claim_4_score_min=None, asmt_claim_4_score_max=None, asmt_claim_4_score_weight=None,
                 asmt_cut_point_1=None, asmt_cut_point_2=None, asmt_cut_point_3=None, asmt_cut_point_4=None,
                 claim_cut_point_1=None, claim_cut_point_2=None,
                 to_date=None, asmt_claim_perf_lvl_name_1=None, asmt_claim_perf_lvl_name_2=None,
                 asmt_claim_perf_lvl_name_3=None):
        '''
        Constructor
        '''

        self.asmt_rec_id = asmt_rec_id
        self.asmt_guid = asmt_guid
        self.asmt_type = asmt_type
        self.asmt_period = asmt_period
        self.asmt_period_year = asmt_period_year
        self.asmt_version = asmt_version
        self.asmt_subject = asmt_subject
        self.asmt_grade = asmt_grade
        self.from_date = from_date

        self.asmt_claim_1_name = asmt_claim_1_name
        self.asmt_claim_2_name = asmt_claim_2_name
        self.asmt_claim_3_name = asmt_claim_3_name
        self.asmt_claim_4_name = asmt_claim_4_name

        self.asmt_perf_lvl_name_1 = asmt_perf_lvl_name_1
        self.asmt_perf_lvl_name_2 = asmt_perf_lvl_name_2
        self.asmt_perf_lvl_name_3 = asmt_perf_lvl_name_3
        self.asmt_perf_lvl_name_4 = asmt_perf_lvl_name_4
        self.asmt_perf_lvl_name_5 = asmt_perf_lvl_name_5

        self.asmt_score_min = asmt_score_min
        self.asmt_score_max = asmt_score_max

        self.asmt_claim_1_score_min = asmt_claim_1_score_min
        self.asmt_claim_1_score_max = asmt_claim_1_score_max
        self.asmt_claim_1_score_weight = asmt_claim_1_score_weight

        self.asmt_claim_2_score_min = asmt_claim_2_score_min
        self.asmt_claim_2_score_max = asmt_claim_2_score_max
        self.asmt_claim_2_score_weight = asmt_claim_2_score_weight

        self.asmt_claim_3_score_min = asmt_claim_3_score_min
        self.asmt_claim_3_score_max = asmt_claim_3_score_max
        self.asmt_claim_3_score_weight = asmt_claim_3_score_weight

        self.asmt_claim_4_score_min = asmt_claim_4_score_min
        self.asmt_claim_4_score_max = asmt_claim_4_score_max
        self.asmt_claim_4_score_weight = asmt_claim_4_score_weight

        self.asmt_cut_point_1 = asmt_cut_point_1
        self.asmt_cut_point_2 = asmt_cut_point_2
        self.asmt_cut_point_3 = asmt_cut_point_3
        self.asmt_cut_point_4 = asmt_cut_point_4

        self.claim_cut_point_1 = claim_cut_point_1
        self.claim_cut_point_2 = claim_cut_point_2

        self.to_date = to_date
        self.most_recent = most_recent

        self.asmt_claim_perf_lvl_name_1 = asmt_claim_perf_lvl_name_1
        self.asmt_claim_perf_lvl_name_2 = asmt_claim_perf_lvl_name_2
        self.asmt_claim_perf_lvl_name_3 = asmt_claim_perf_lvl_name_3

    def __str__(self):
        '''
        toString Method
        '''
        return ("Assessment:[asmt_type: %s, subject: %s, asmt_type: %s, period: %s, version: %s, grade: %s]" % (self.asmt_type, self.asmt_subject, self.asmt_type, self.asmt_period, self.asmt_version, self.asmt_grade))

    def getRow(self):
        return [self.asmt_rec_id, self.asmt_guid, self.asmt_type, self.asmt_period, self.asmt_period_year, self.asmt_version, self.asmt_subject,
                self.asmt_claim_1_name, self.asmt_claim_2_name, self.asmt_claim_3_name, self.asmt_claim_4_name,
                self.asmt_perf_lvl_name_1, self.asmt_perf_lvl_name_2, self.asmt_perf_lvl_name_3, self.asmt_perf_lvl_name_4, self.asmt_perf_lvl_name_5,
                self.asmt_score_min, self.asmt_score_max,
                self.asmt_claim_1_score_min, self.asmt_claim_1_score_max, self.asmt_claim_1_score_weight, self.asmt_claim_perf_lvl_name_1,
                self.asmt_claim_2_score_min, self.asmt_claim_2_score_max, self.asmt_claim_2_score_weight, self.asmt_claim_perf_lvl_name_2,
                self.asmt_claim_3_score_min, self.asmt_claim_3_score_max, self.asmt_claim_3_score_weight, self.asmt_claim_perf_lvl_name_3,
                self.asmt_claim_4_score_min, self.asmt_claim_4_score_max, self.asmt_claim_4_score_weight,
                self.asmt_cut_point_1, self.asmt_cut_point_2, self.asmt_cut_point_3, self.asmt_cut_point_4,
                self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['asmt_rec_id', 'asmt_guid', 'asmt_type', 'asmt_period', 'asmt_period_year', 'asmt_version', 'asmt_subject',
                'asmt_claim_1_name', 'asmt_claim_2_name', 'asmt_claim_3_name', 'asmt_claim_4_name',
                'asmt_perf_lvl_name_1', 'asmt_perf_lvl_name_2', 'asmt_perf_lvl_name_3', 'asmt_perf_lvl_name_4', 'asmt_perf_lvl_name_5',
                'asmt_score_min', 'asmt_score_max',
                'asmt_claim_1_score_min', 'asmt_claim_1_score_max', 'asmt_claim_1_score_weight', 'asmt_claim_perf_lvl_name_1',
                'asmt_claim_2_score_min', 'asmt_claim_2_score_max', 'asmt_claim_2_score_weight', 'asmt_claim_perf_lvl_name_2',
                'asmt_claim_3_score_min', 'asmt_claim_3_score_max', 'asmt_claim_3_score_weight', 'asmt_claim_perf_lvl_name_3',
                'asmt_claim_4_score_min', 'asmt_claim_4_score_max', 'asmt_claim_4_score_weight',
                'asmt_cut_point_1', 'asmt_cut_point_2', 'asmt_cut_point_3', 'asmt_cut_point_4',
                'from_date', 'to_date', 'most_recent']


class AssessmentOutcome(object):

    def __init__(self, asmnt_outcome_rec_id, asmt_rec_id, student_id,
                 teacher_guid, state_code, district_id, school_id, section_guid, inst_hier_rec_id, section_rec_id,
                 where_taken_id, where_taken_name, asmt_grade, enrl_grade, date_taken, date_taken_day,
                 date_taken_month, date_taken_year,
                 asmt_score, asmt_score_range_min, asmt_score_range_max, asmt_perf_lvl,
                 asmt_claim_1_score, asmt_claim_1_score_range_min, asmt_claim_1_score_range_max, asmt_claim_1_perf_lvl,
                 asmt_claim_2_score, asmt_claim_2_score_range_min, asmt_claim_2_score_range_max, asmt_claim_2_perf_lvl,
                 asmt_claim_3_score, asmt_claim_3_score_range_min, asmt_claim_3_score_range_max, asmt_claim_3_perf_lvl,
                 asmt_claim_4_score, asmt_claim_4_score_range_min, asmt_claim_4_score_range_max, asmt_claim_4_perf_lvl,
                 status, most_recent, batch_guid, asmt_type, asmt_year, asmt_subject, gender,
                 dmg_eth_hsp=False, dmg_eth_ami=False, dmg_eth_asn=False, dmg_eth_blk=False,
                 dmg_eth_pcf=False, dmg_eth_wht=False, dmg_prg_iep=False, dmg_prg_lep=False,
                 dmg_prg_504=False, dmg_prg_tt1=False, dmg_eth_derived=None):

        self.asmnt_outcome_rec_id = asmnt_outcome_rec_id
        self.asmt_rec_id = asmt_rec_id
        self.student_id = student_id
        self.teacher_guid = teacher_guid
        self.state_code = state_code
        self.district_id = district_id
        self.school_id = school_id
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

        self.gender = gender

        # Overall Assessment Data
        self.asmt_score = asmt_score
        self.asmt_score_range_min = asmt_score_range_min
        self.asmt_score_range_max = asmt_score_range_max
        self.asmt_perf_lvl = asmt_perf_lvl

        # General Assessment info
        self.asmt_type = asmt_type
        self.asmt_year = asmt_year
        self.asmt_subject = asmt_subject

        # Assessment Claim Data
        self.asmt_claim_1_score = asmt_claim_1_score
        self.asmt_claim_1_score_range_min = asmt_claim_1_score_range_min
        self.asmt_claim_1_score_range_max = asmt_claim_1_score_range_max
        self.asmt_claim_1_perf_lvl = asmt_claim_1_perf_lvl

        self.asmt_claim_2_score = asmt_claim_2_score
        self.asmt_claim_2_score_range_min = asmt_claim_2_score_range_min
        self.asmt_claim_2_score_range_max = asmt_claim_2_score_range_max
        self.asmt_claim_2_perf_lvl = asmt_claim_2_perf_lvl

        self.asmt_claim_3_score = asmt_claim_3_score
        self.asmt_claim_3_score_range_min = asmt_claim_3_score_range_min
        self.asmt_claim_3_score_range_max = asmt_claim_3_score_range_max
        self.asmt_claim_3_perf_lvl = asmt_claim_3_perf_lvl

        self.asmt_claim_4_score = asmt_claim_4_score
        self.asmt_claim_4_score_range_min = asmt_claim_4_score_range_min
        self.asmt_claim_4_score_range_max = asmt_claim_4_score_range_max
        self.asmt_claim_4_perf_lvl = asmt_claim_4_perf_lvl

        self.status = status
        self.most_recent = most_recent
        self.batch_guid = batch_guid

        # Demographic Data
        self.dmg_eth_hsp = dmg_eth_hsp
        self.dmg_eth_ami = dmg_eth_ami
        self.dmg_eth_asn = dmg_eth_asn
        self.dmg_eth_blk = dmg_eth_blk
        self.dmg_eth_pcf = dmg_eth_pcf
        self.dmg_eth_wht = dmg_eth_wht
        self.dmg_prg_iep = dmg_prg_iep
        self.dmg_prg_lep = dmg_prg_lep
        self.dmg_prg_504 = dmg_prg_504
        self.dmg_prg_tt1 = dmg_prg_tt1
        self.dmg_eth_derived = dmg_eth_derived

    def getRow(self):
        return [self.asmnt_outcome_rec_id, self.asmt_rec_id,
                self.student_id, self.state_code,  # removed: self.teacher_guid,
                self.district_id, self.school_id, self.section_guid,
                self.inst_hier_rec_id, self.section_rec_id,
                self.where_taken_id, self.where_taken_name, self.asmt_grade, self.enrl_grade,
                self.date_taken, self.date_taken_day, self.date_taken_month, self.date_taken_year,
                self.asmt_score, self.asmt_score_range_min, self.asmt_score_range_max,
                self.asmt_perf_lvl,
                self.asmt_claim_1_score, self.asmt_claim_1_score_range_min, self.asmt_claim_1_score_range_max, self.asmt_claim_1_perf_lvl,
                self.asmt_claim_2_score, self.asmt_claim_2_score_range_min, self.asmt_claim_2_score_range_max, self.asmt_claim_2_perf_lvl,
                self.asmt_claim_3_score, self.asmt_claim_3_score_range_min, self.asmt_claim_3_score_range_max, self.asmt_claim_3_perf_lvl,
                self.asmt_claim_4_score, self.asmt_claim_4_score_range_min, self.asmt_claim_4_score_range_max, self.asmt_claim_4_perf_lvl,
                self.status, self.most_recent, self.batch_guid,
                self.asmt_type, self.asmt_year, self.asmt_subject, self.gender,
                self.dmg_eth_hsp, self.dmg_eth_ami, self.dmg_eth_asn, self.dmg_eth_blk,
                self.dmg_eth_pcf, self.dmg_eth_wht, self.dmg_prg_iep,
                self.dmg_prg_lep, self.dmg_prg_504, self.dmg_prg_tt1, self.dmg_eth_derived]

    @classmethod
    def getHeader(cls):
        return ['asmnt_outcome_rec_id', 'asmt_rec_id',
                'student_id', 'state_code',  # removed: 'teacher_guid',
                'district_id', 'school_id', 'section_guid',
                'inst_hier_rec_id', 'section_rec_id',
                'where_taken_id', 'where_taken_name', 'asmt_grade', 'enrl_grade',
                'date_taken', 'date_taken_day', 'date_taken_month', 'date_taken_year',
                'asmt_score', 'asmt_score_range_min', 'asmt_score_range_max', 'asmt_perf_lvl',
                'asmt_claim_1_score', 'asmt_claim_1_score_range_min', 'asmt_claim_1_score_range_max', 'asmt_claim_1_perf_lvl',
                'asmt_claim_2_score', 'asmt_claim_2_score_range_min', 'asmt_claim_2_score_range_max', 'asmt_claim_2_perf_lvl',
                'asmt_claim_3_score', 'asmt_claim_3_score_range_min', 'asmt_claim_3_score_range_max', 'asmt_claim_3_perf_lvl',
                'asmt_claim_4_score', 'asmt_claim_4_score_range_min', 'asmt_claim_4_score_range_max', 'asmt_claim_4_perf_lvl',
                'status', 'most_recent', 'batch_guid',
                'asmt_type', 'asmt_year', 'asmt_subject', 'gender',
                'dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf',
                'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1', 'dmg_eth_derived']


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

    def __init__(self, staff_rec_id, staff_guid, first_name, last_name, section_guid, hier_user_type, state_code,
                 district_id, school_id, from_date, most_recent, to_date=None, middle_name=None):
        super().__init__(first_name, last_name, middle_name=middle_name)
        self.staff_rec_id = staff_rec_id
        self.staff_guid = staff_guid
        self.section_guid = section_guid
        self.hier_user_type = hier_user_type
        self.state_code = state_code
        self.district_id = district_id
        self.school_id = school_id
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

    def getRow(self):
        return [self.staff_rec_id, self.staff_guid, self.first_name, self.middle_name, self.last_name, self.section_guid, self.hier_user_type, self.state_code, self.district_id, self.school_id, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['staff_rec_id', 'staff_guid', 'first_name', 'middle_name', 'last_name', 'section_guid', 'hier_user_type', 'state_code', 'district_id', 'school_id', 'from_date', 'to_date', 'most_recent']


class ExternalUserStudent():
    '''
    ExternalUserStudent Object
    '''

    def __init__(self, external_user_student_id, external_user_guid, student_id, from_date, to_date=None):
        self.external_user_student_id = external_user_student_id
        self.external_user_guid = external_user_guid
        self.student_id = student_id
        self.from_date = from_date
        self.to_date = to_date

    def getRow(self):
        return [self.external_user_student_id, self.external_user_guid, self.student_id, self.from_date, self.to_date]

    @classmethod
    def getHeader(cls):
        return ['external_user_student_id', 'external_user_guid', 'student_id', 'from_date', 'to_date']


class Student():
    '''
        Student Object maps to dim_student table
    '''

    def __init__(self, student_rec_id, student_id, first_name, last_name, address_1, city, zip_code,
                 gender, email, dob,
                 section_guid, grade, state_code, district_id, school_id, from_date, most_recent,
                 middle_name=None, address_2=None, to_date=None):

        self.student_rec_id = student_rec_id
        self.student_id = student_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.zip_code = zip_code
        self.gender = gender
        self.email = email
        self.dob = dob
        self.section_guid = section_guid
        self.grade = grade
        self.state_code = state_code
        self.district_id = district_id
        self.school_id = school_id
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent
        self.has_updated_gender = False

    def getRow(self):
        return [self.student_rec_id, self.student_id, self.first_name, self.middle_name, self.last_name, self.address_1, self.address_2,
                self.city, self.zip_code, self.gender, self.email, self.dob, self.section_guid, self.grade,
                self.state_code, self.district_id, self.school_id, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['student_rec_id', 'student_id', 'first_name', 'middle_name', 'last_name', 'address_1', 'address_2',
                'city', 'zip_code', 'gender', 'email', 'dob', 'section_guid', 'grade',
                'state_code', 'district_id', 'school_id', 'from_date', 'to_date', 'most_recent']
