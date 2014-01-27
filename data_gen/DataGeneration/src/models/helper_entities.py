import random
from uuid import uuid4
from DataGeneration.src.generators.generate_names import (generate_first_or_middle_name, generate_last_name,
                                                          possibly_generate_middle_name)
import DataGeneration.src.utils.util as util
from DataGeneration.src.demographics.demographic_derived import derive_demographic as get_derived_demographic


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
    def __init__(self, claim_score, claim_score_interval_minimum, claim_score_interval_maximum, perf_lvl):
        self.claim_score = claim_score
        self.claim_score_interval_minimum = claim_score_interval_minimum
        self.claim_score_interval_maximum = claim_score_interval_maximum
        self.perf_lvl = perf_lvl


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
                 dmg_prg_504=False, dmg_prg_tt1=False, dmg_eth_2mr=False, dmg_eth_nst=False, student_guid=None,
                 first_name=None, middle_name=None, last_name=None, zip_code=None, dob=None, student_rec_ids=None,
                 email=None, address_1=None, address_2=None, city=None, state_code=None, district_guid=None,
                 school_guid=None, from_date=None, to_date=None, most_recent=None, asmt_rec_ids=None, asmt_guids=None,
                 section_guids=None, section_rec_ids=None, teacher_guids=None, teachers=None, asmt_dates_taken=None,
                 asmt_types=None, asmt_subjects=None, asmt_years=None):
        '''
        Create an unassignedStudent object and populate with name, address, and dob based on the gender and grade.
        Other demographics are optional at initialization.
        @param asmt_scores: A dictionary of asmt_scores where the keys are the subject for the assessment
        @type asmt_scores: dict
        '''

        self.grade = grade
        self.gender = gender
        self.student_guid = student_guid if student_guid else uuid4()
        self.first_name = first_name if first_name else generate_first_or_middle_name(gender)
        self.middle_name = middle_name if middle_name else possibly_generate_middle_name(gender)
        self.last_name = last_name if last_name else generate_last_name()

        # TODO: implement city-zip map
        self.zip_code = zip_code if zip_code else random.randint(10000, 99999)
        self.dob = dob if dob else util.generate_dob(grade)

        # data to be set after initialization
        self.student_rec_ids = student_rec_ids if student_rec_ids else {}
        self.email = email
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.state_code = state_code
        self.district_guid = district_guid
        self.school_guid = school_guid
        self.from_date = from_date
        self.to_date = to_date
        self.most_recent = most_recent

        # Demographic Data
        self.dmg_eth_hsp = dmg_eth_hsp
        self.dmg_eth_ami = dmg_eth_ami
        self.dmg_eth_asn = dmg_eth_asn
        self.dmg_eth_blk = dmg_eth_blk
        self.dmg_eth_pcf = dmg_eth_pcf
        self.dmg_eth_wht = dmg_eth_wht
        self.dmg_eth_2mr = dmg_eth_2mr
        self.dmg_eth_nst = dmg_eth_nst
        self.dmg_prg_iep = dmg_prg_iep
        self.dmg_prg_lep = dmg_prg_lep
        self.dmg_prg_504 = dmg_prg_504
        self.dmg_prg_tt1 = dmg_prg_tt1

        # a dict that contains an assessment score object that corresponds to each subject
        self.asmt_scores = asmt_scores
        self.asmt_rec_ids = asmt_rec_ids if asmt_rec_ids else {}
        self.asmt_guids = asmt_guids if asmt_guids else {}
        self.section_guids = section_guids if section_guids else {}
        self.section_rec_ids = section_rec_ids if section_rec_ids else {}
        self.teacher_guids = teacher_guids if teacher_guids else {}
        self.teachers = teachers if teachers else {}
        self.asmt_dates_taken = asmt_dates_taken if asmt_dates_taken else {}

        # New Assessment Information
        self.asmt_types = asmt_types if asmt_years else {}
        self.asmt_subjects = asmt_subjects if asmt_subjects else {}
        self.asmt_years = asmt_years if asmt_years else {}

        self.asmt_dicts_stored_by_guid = [self.asmt_scores, self.asmt_rec_ids, self.asmt_guids, self.asmt_dates_taken,
                                          self.asmt_types, self.asmt_subjects, self.asmt_years]

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

        # if the student has 2mr set then assign them two ethnicities
        if 'dmg_eth_2mr' in student_demo:
            # we do not want dmg_eth_2mr to be counted as a demographic
            student_demos = random.sample(['dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_ami', 'dmg_eth_pcf', 'dmg_eth_wht'], 2)
            for demo in student_demos:
                setattr(self, demo, True)

    def get_stu_demo_list(self):
        '''
        Returns a list of boolean values for each demographic. The order is:
        1. African American,
        2. Asian,
        3. Hispanic,
        4. Native American / Alaskan Native,
        5. Pacific Islander,
        6. White
        '''
        return [self.dmg_eth_blk, self.dmg_eth_asn, self.dmg_eth_hsp, self.dmg_eth_ami, self.dmg_eth_pcf, self.dmg_eth_wht]

    def derived_demographic(self):
        """
        Return the derived demographic based on the students list of demographics
        :return: An integer value denoting the demographic
        """
        return get_derived_demographic(self.get_stu_demo_list())

    def delete_assessment_info(self, asmt_guid):
        """
        remove all information stored in this object about the assessment with the given guid
        :param asmt_guid: a UUID object representing the guid for the assessment
        :return: None
        """
        try:
            for attribute in self.asmt_dicts_stored_by_guid:
                del attribute[asmt_guid]
        except KeyError:
            print('Key error in deleting assessment information in student')
            print('attribute name', attribute)
            raise
