import random
from uuid import uuid4
from DataGeneration.src.generate_names import (generate_first_or_middle_name, generate_last_name,
                                               possibly_generate_middle_name)
import DataGeneration.src.util as util


class State:
    '''
    State object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, state_name, state_code, districts=None, state_type=None):
        '''
        Constructor
        '''
        self.state_code = state_code
        self.state_name = state_name
        self.state_type = state_type
        self.districts = districts
        self.staff = None


class District:
    '''
    District object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, district_guid, district_name, district_type=None, school_populations=None):
        '''
        Constructor
        '''
        self.district_guid = district_guid
        self.district_name = district_name
        self.district_type = district_type
        self.school_populations = school_populations
        self.schools = None
        self.staff = None


class School:
    '''
    School Object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, school_guid, school_name, school_category, grade_performance_level_counts, district_name, district_guid):
        self.school_guid = school_guid
        self.school_name = school_name
        self.school_category = school_category
        self.grade_performance_level_counts = grade_performance_level_counts
        self.district_name = district_name
        self.district_guid = district_guid
        self.student_info = None
        self.teachers = None
        self.sections = None


class Claim:
    '''
    claim information to be used by the assessment object. Simply defines basic parameters about claim.
    '''
    def __init__(self, claim_name, claim_score_min, claim_score_max, claim_score_weight):
        self.claim_name = claim_name
        self.claim_score_min = claim_score_min
        self.claim_score_max = claim_score_max
        self.claim_score_weight = claim_score_weight


class ClaimScore():
    '''
    This is a claim object with scores. Used to create assessment_outcome row.
    '''
    def __init__(self, claim_score, claim_score_interval_minimum, claim_score_interval_maximum):
        self.claim_score = claim_score
        self.claim_score_interval_minimum = claim_score_interval_minimum
        self.claim_score_interval_maximum = claim_score_interval_maximum


class AssessmentScore:
    '''
    Assessment Score object
    '''
    def __init__(self, overall_score, perf_lvl, interval_min, interval_max, claim_scores, asmt_create_date):
        '''
        Constructor
        '''
        self.overall_score = overall_score
        self.perf_lvl = perf_lvl
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.claim_scores = claim_scores
        self.asmt_create_date = asmt_create_date

    def __str__(self):
        '''
        String method
        '''
        return ("Score:[overall: %s, claims: %s]" % (self.overall_score, self.claim_scores))


class StudentInfo(object):
    '''
    StudentInfo.
    Object to hold a student that has scores and demographic information but does not yet have
    school information
    '''

    def __init__(self, grade, gender, asmt_scores, dmg_eth_hsp=False, dmg_eth_ami=False, dmg_eth_asn=False,
                 dmg_eth_blk=False, dmg_eth_pcf=False, dmg_eth_wht=False, dmg_prg_iep=False, dmg_prg_lep=False,
                 dmg_prg_504=False, dmg_prg_tt1=False):
        '''
        Create an unassignedStudent object and populate with name, address, and dob based on the gender and grade.
        Other demographics are optional at initialization.
        @param asmt_scores: A dictionary of asmt_scores where the keys are the subject for the assessment
        @type asmt_scores: dict
        '''

        self.grade = grade
        self.gender = gender
        self.student_guid = uuid4()
        self.first_name = generate_first_or_middle_name(gender)
        self.middle_name = possibly_generate_middle_name(gender)
        self.last_name = generate_last_name()

        # TODO: implement city-zip map
        self.zip_code = random.randint(10000, 99999)
        # self.email = util.generate_email_address(self.first_name, self.last_name, self.school_name)
        self.dob = util.generate_dob(grade)

        # data to be set after initialization
        self.student_rec_ids = None
        self.email = None
        self.address_1 = None
        self.addres_2 = None
        self.city = None
        self.state_code = None
        self.district_guid = None
        self.school_guid = None
        self.from_date = None
        self.to_date = None
        self.most_recent = None

        # Demographic Data
        self.dmg_eth_hsp = dmg_eth_hsp
        self.dmg_eth_ami = dmg_eth_ami
        self.dmg_eth_asn = dmg_eth_asn
        self.dmg_eth_blk = dmg_eth_blk
        self.dmg_eth_pcf = dmg_eth_pcf
        self.dmg_eth_wht = dmg_eth_wht
        self.dmg_eth_2mr = False
        self.dmg_eth_nst = False
        self.dmg_prg_iep = dmg_prg_iep
        self.dmg_prg_lep = dmg_prg_lep
        self.dmg_prg_504 = dmg_prg_504
        self.dmg_prg_tt1 = dmg_prg_tt1

        # a dict that contains an assessment score object that corresponds to each subject
        self.asmt_scores = asmt_scores
        self.asmt_rec_ids = {}
        self.section_guids = {}
        self.section_rec_ids = {}
        self.teacher_guids = {}
        self.asmt_dates_taken = {}

    def set_additional_info(self, student_rec_id, email, address_1, city, section_guid, state_code, district_guid,
                            school_guid, from_date, to_date, most_recent, address_2=None):
        '''
        Set the additional student info that may not be available at object creation
        '''
        self.student_rec_id = student_rec_id
        self.email = email
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.section_guid = section_guid
        self.state_code = state_code
        self.district_guid = district_guid
        self.school_guid = school_guid
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

    def getDemoOfStudent(self, substr='dmg'):
        demo = []
        for attr_name in self.__dict__:
            if substr in attr_name and self.__dict__[attr_name] is True:
                demo.append(attr_name)

        demo.append(self.gender)

        return demo

    def set_dmg_eth_2mr(self):
        '''
        Set the value for dmg_eth_2mr
        '''
        student_demo = self.getDemoOfStudent('dmg_eth')
        if 'dmg_eth_2mr' in student_demo:
            # we do not want dmg_eth_2mr to be counted as a demographic
            student_demo.remove('dmg_eth_2mr')
        # since there is a gender value in student_demo. two or more races means len(student_demo) > 2
        if len(student_demo) > 2 and 'dmg_eth_hsp' not in student_demo:
            self.dmg_eth_2mr = True
        else:
            self.dmg_eth_2mr = False


class StudentBioInfo:

    def __init__(self, student_guid, first_name, last_name, address_1, dob, district_guid, state_code, gender, email, school_guid, zip_code, city, middle_name=None, address_2=None):

        super().__init__(first_name, last_name, middle_name=middle_name)

        # Ids can either be given to the constructor or provided by constructor
        # Either way, both Id fields must have a value
        id_generator = IdGen()
        if student_guid is None:
            self.student_guid = id_generator.get_id()
        else:
            self.student_guid = student_guid
        if student_rec_id is None:
            self.student_rec_id = id_generator.get_id()
        else:
            self.student_rec_id = student_rec_id

        self.address_1 = address_1
        self.address_2 = address_2
        self.dob = dob
        self.district_guid = district_guid
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code
        self.gender = gender
        self.email = email
        self.school_guid = school_guid
