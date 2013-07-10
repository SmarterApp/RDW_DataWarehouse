__author__ = 'abrien'

from uuid import uuid4

from idgen import IdGen
from constants import MAXIMUM_ASSESSMENT_SCORE, MINIMUM_ASSESSMENT_SCORE, AVERAGE_ASSESSMENT_SCORE, ASSESSMENT_SCORE_STANDARD_DEVIATION


# TODO: get rid of camel-cased function names
class InstitutionHierarchy:
    '''
    Institution Hierarchy object
    '''

    def __init__(self, inst_hier_rec_id, state_name, state_code, district_guid, district_name, school_guid, school_name, school_category,
                 from_date, most_recent, to_date=None):

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
        '''
        Returns the information stored in this object as csv row
        '''
        return [self.inst_hier_rec_id, self.state_name, self.state_code, self.district_guid, self.district_name, self.school_guid, self.school_name, self.school_category, self.from_date, self.to_date, self.most_recent]

    # TODO: For all these getHeader methods, there must be a better way to return a list of the fields (in a defined order)
    # hard coding probably is not the best approach
    @classmethod
    def getHeader(cls):
        '''
        Returns the csv of header of this entity
        '''
        return ['inst_hier_rec_id', 'state_name', 'state_code', 'district_guid', 'district_name', 'school_guid', 'school_name', 'school_category', 'from_date', 'to_date', 'most_recent']


class Section:
    '''
    Section Object
    '''
    def __init__(self, section_rec_id, section_guid, section_name, grade, class_name, subject_name, state_code, district_guid, school_guid, from_date, most_recent, to_date=None):

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
    def __init__(self, asmt_rec_id, asmt_guid, asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_subject,
                 asmt_grade, from_date, most_recent,
                 asmt_claim_1_name=None, asmt_claim_2_name=None, asmt_claim_3_name=None, asmt_claim_4_name=None,
                 asmt_perf_lvl_name_1=None, asmt_perf_lvl_name_2=None, asmt_perf_lvl_name_3=None, asmt_perf_lvl_name_4=None, asmt_perf_lvl_name_5=None,
                 asmt_score_min=None, asmt_score_max=None,
                 asmt_claim_1_score_min=None, asmt_claim_1_score_max=None, asmt_claim_1_score_weight=None,
                 asmt_claim_2_score_min=None, asmt_claim_2_score_max=None, asmt_claim_2_score_weight=None,
                 asmt_claim_3_score_min=None, asmt_claim_3_score_max=None, asmt_claim_3_score_weight=None,
                 asmt_claim_4_score_min=None, asmt_claim_4_score_max=None, asmt_claim_4_score_weight=None,
                 asmt_custom_metadata=None,
                 asmt_cut_point_1=None, asmt_cut_point_2=None, asmt_cut_point_3=None, asmt_cut_point_4=None,
                 to_date=None):
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

        self.asmt_custom_metadata = asmt_custom_metadata

        self.to_date = to_date
        self.most_recent = most_recent

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
                self.asmt_claim_1_score_min, self.asmt_claim_1_score_max, self.asmt_claim_1_score_weight,
                self.asmt_claim_2_score_min, self.asmt_claim_2_score_max, self.asmt_claim_2_score_weight,
                self.asmt_claim_3_score_min, self.asmt_claim_3_score_max, self.asmt_claim_3_score_weight,
                self.asmt_claim_4_score_min, self.asmt_claim_4_score_max, self.asmt_claim_4_score_weight,
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
                 asmt_create_date, status, most_recent, dmg_eth_hsp='N', dmg_eth_ami='N', dmg_eth_asn='N',
                 dmg_eth_blk='N', dmg_eth_pcf='N', dmg_eth_wht='N', dmg_prg_iep='N', dmg_prg_lep='N',
                 dmg_prg_504='N', dmg_prg_tt1='N'):

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

        self.asmt_claim_4_score = asmt_claim_4_score
        self.asmt_claim_4_score_range_min = asmt_claim_4_score_range_min
        self.asmt_claim_4_score_range_max = asmt_claim_4_score_range_max

        self.asmt_create_date = asmt_create_date
        self.status = status
        self.most_recent = most_recent

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

    def set_demograph(self, dmg_eth_hsp=None, dmg_eth_ami=None, dmg_eth_asn=None, dmg_eth_blk=None, dmg_eth_pcf=None, dmg_eth_wht=None,
                      dmg_prg_iep=None, dmg_prg_lep=None, dmg_prg_504=None, dmg_prg_tt1=None):

        self.dmg_eth_hsp = dmg_eth_hsp if dmg_eth_hsp is not None else self.dmg_eth_hsp
        self.dmg_eth_ami = dmg_eth_ami if dmg_eth_ami is not None else self.dmg_eth_ami
        self.dmg_eth_asn = dmg_eth_asn if dmg_eth_asn is not None else self.dmg_eth_asn
        self.dmg_eth_blk = dmg_eth_blk if dmg_eth_blk is not None else self.dmg_eth_blk
        self.dmg_eth_pcf = dmg_eth_pcf if dmg_eth_pcf is not None else self.dmg_eth_pcf
        self.dmg_eth_wht = dmg_eth_wht if dmg_eth_wht is not None else self.dmg_eth_wht
        self.dmg_prg_iep = dmg_prg_iep if dmg_prg_iep is not None else self.dmg_prg_iep
        self.dmg_prg_lep = dmg_prg_lep if dmg_prg_lep is not None else self.dmg_prg_lep
        self.dmg_prg_504 = dmg_prg_504 if dmg_prg_504 is not None else self.dmg_prg_504
        self.dmg_prg_tt1 = dmg_prg_tt1 if dmg_prg_tt1 is not None else self.dmg_prg_tt1

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
                self.asmt_create_date, self.status, self.most_recent, self.dmg_eth_hsp, self.dmg_eth_ami,
                self.dmg_eth_asn, self.dmg_eth_blk, self.dmg_eth_pcf, self.dmg_eth_wht, self.dmg_prg_iep,
                self.dmg_prg_lep, self.dmg_prg_504, self.dmg_prg_tt1]

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
                'asmt_create_date', 'status', 'most_recent', 'dmt_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn',
                'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1']


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
                 district_guid, school_guid, from_date, most_recent, to_date=None, middle_name=None):
        super().__init__(first_name, last_name, middle_name=middle_name)
        self.staff_rec_id = staff_rec_id
        self.staff_guid = staff_guid
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
    '''

    def __init__(self, external_user_student_guid, external_user_guid, student_guid, from_date, to_date=None):
        self.external_user_student_guid = external_user_student_guid
        self.external_user_guid = external_user_guid
        self.student_guid = student_guid
        self.from_date = from_date
        self.to_date = to_date

    def getRow(self):
        return [self.external_user_student_guid, self.external_user_guid, self.student_guid, self.from_date, self.to_date]

    @classmethod
    def getHeader(cls):
        return ['external_user_student_guid', 'external_user_guid', 'student_guid', 'from_date', 'to_date']


class Student():
    '''
        Student Object maps to dim_student table
    '''

    def __init__(self, student_rec_id, student_guid, first_name, last_name, address_1, city, zip_code,
                 gender, email, dob,
                 section_guid, grade, state_code, district_guid, school_guid, from_date, most_recent,
                 middle_name=None, address_2=None, to_date=None, dmg_eth_hsp='N', dmg_eth_ami='N', dmg_eth_asn='N',
                 dmg_eth_blk='N', dmg_eth_pcf='N', dmg_eth_wht='N', dmg_prg_iep='N', dmg_prg_lep='N',
                 dmg_prg_504='N', dmg_prg_tt1='N'):

        self.student_rec_id = student_rec_id
        self.student_guid = student_guid
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
        self.district_guid = district_guid
        self.school_guid = school_guid
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent
        self.has_updated_gender = False

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
        self.demographics_assigned = False

    def getDemoOfStudent(self):
        demo = []
        if self.dmg_eth_hsp is True:
            demo.append('dmg_eth_hsp')
        if self.dmg_eth_ami is True:
            demo.append('dmg_eth_ami')
        if self.dmg_eth_asn is True:
            demo.append('dmg_eth_asn')
        if self.dmg_eth_blk is True:
            demo.append('dmg_eth_blk')
        if self.dmg_eth_pcf is True:
            demo.append('dmg_eth_pcf')
        if self.dmg_eth_wht is True:
            demo.append('dmg_eth_wht')
        if self.dmg_prg_iep is True:
            demo.append('dmg_prg_iep')
        if self.dmg_prg_lep is True:
            demo.append('dmg_prg_lep')
        if self.dmg_prg_504 is True:
            demo.append('dmg_prg_504')
        if self.dmg_prg_tt1 is True:
            demo.append('dmg_prg_tt1')
        demo.append(self.gender)
        return demo

    def getRow(self):
        return [self.student_rec_id, self.student_guid, self.first_name, self.middle_name, self.last_name, self.address_1, self.address_2,
                self.city, self.zip_code, self.gender, self.email, self.dob, self.section_guid, self.grade,
                self.state_code, self.district_guid, self.school_guid, self.from_date, self.to_date, self.most_recent]

    @classmethod
    def getHeader(cls):
        return ['student_rec_id', 'student_guid', 'first_name', 'middle_name', 'last_name', 'address_1', 'address_2',
                'city', 'zip_code', 'gender', 'email', 'dob', 'section_guid', 'grade',
                'state_code', 'district_guid', 'school_guid', 'from_date', 'to_date', 'most_recent']
