'''
Created on Sep 18, 2013

@author: swimberly
'''

import os
import json
import copy
from collections import OrderedDict

from DataGeneration.src.writers.write_to_csv import create_csv, prepare_csv_files
from DataGeneration.src.models.helper_entities import ClaimScore, AssessmentScore, State, StudentInfo, School
from DataGeneration.src.models.entities import Staff


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
JSONFILE = os.path.join(__location__, '..', '..', 'datafiles', 'mappings.json')

LANDING_ZONE_FILE_PATTERN = 'REALDATA_ASMT_ID_{0}.csv'
LANDING_ZONE_SINGLE_FILE = 'REALDATA_RECORDS.csv'
JSON_PATTERN = 'METADATA_ASMT_ID_{0}.json'
IDENTIFICATION = 'identification'
ID = 'id'
GUID = 'guid'
OVERALL = 'overall'
CLAIMS = 'claims'
PERFORMANCE = 'performance_levels'
CLAIM_PERFORMANCE = 'claim_performance_levels'


def output_generated_asmts_to_json(assessments, output_dict):
    '''
    Given a list of assessemtns and the output_dictionary. Write the assessment data to a json file
    '''
    file_path = get_file_path_from_output_dict(output_dict)
    mappings = read_mapping_json(JSONFILE)
    for asmt in assessments:
        generate_json(asmt, mappings, file_path, JSON_PATTERN)


def generate_json(assessment, mappings, output_path, filename_pattern):
    '''
    @param data_dict: A dictionary containing the content for the output json file
    @param mappings: A dictionary that contains what the json keys should map to
    @param output_path: the path to where the files should be written
    @param filename_pattern: The pattern to be used that can be formatted with the asmt_id
    @return: the asmt_id for the json file that was written
    '''
    # duplicate the mappings dict
    asmt_ord_dict = copy.deepcopy(mappings)

    for json_section in mappings:
        # setup identification and overall sections
        if json_section == IDENTIFICATION or json_section == OVERALL:
            for key, col_name in mappings[json_section].items():
                asmt_ord_dict[json_section][key] = get_val_from_assessment(assessment, col_name)

        elif json_section == PERFORMANCE or json_section == CLAIMS or json_section == CLAIM_PERFORMANCE:
            # loop through list and add vals
            asmt_ord_dict[json_section] = create_list_for_section(mappings[json_section], assessment)

    # write json file
    filename = os.path.join(output_path, filename_pattern.format(asmt_ord_dict[IDENTIFICATION][GUID]))
    write_json_file(asmt_ord_dict, filename)

    return asmt_ord_dict[IDENTIFICATION][GUID]


def create_list_for_section(section_dict, assessment):
    '''
    Creates a list of orderedDicts that make up the section for performance_level
    or Claims
    @param section_dict: the ordered dict that contains the mapping informartion for a section
    @param data_dict: the dict that contains the data for a particular claim or performance level
    @return: a list of OrderedDict elements that contain the proper data
    '''

    res_dict = OrderedDict()

    for num_key in section_dict:
        d = OrderedDict()

        for key, col_name in section_dict[num_key].items():
            d[key] = get_val_from_assessment(assessment, col_name)

        res_dict[num_key] = d

    return res_dict


def get_val_from_assessment(assessment, col_val):
    '''
    Get the given attribute from the assessment object. Return an empty string if the value is None
    '''
    ret_val = getattr(assessment, col_val)
    if ret_val is None:
        return ''
    return str(ret_val)


def write_json_file(ordered_data, filename):
    '''
    write the given OrderedDictionary to a .json file
    @param ordered_data: an OrderedDict containing the data that is to be written to a file
    @param filename: what to name the output json file
    @return: None
    '''
    #new_filename = 'METADATA_' + filename + '.json'

    with open(filename, 'w') as f:
        formatted_json = json.dumps(ordered_data, indent=4)
        f.write(formatted_json)


def read_mapping_json(mapping_file):
    '''
    Open the mapping json file. Read and parse it into an OrderedDict
    @return: an OrderedDict of the json
    '''

    with open(mapping_file, 'r') as f:
        mappings = json.loads(f.read(), object_pairs_hook=OrderedDict)
        return mappings


def output_generated_districts_to_lz_format(districts, state_population, batch_guid, output_dict, from_date, most_recent, to_date, single_file=True):
    '''
    '''

    file_path = get_file_path_from_output_dict(output_dict)

    single_file_key = 1
    real_data_objects = {}

    for district in districts:
        for school in district.schools:
            for student_info in school.student_info:
                student_real_data_objects = create_realdata_objs_from_helper_entities(state_population, school, student_info)
                add_student_realdata_to_dict(student_real_data_objects, real_data_objects, single_file_key, single_file)

    output_real_data_objects(real_data_objects, single_file_key, file_path)


def output_real_data_objects(real_data_objects, single_file_key, file_path):
    '''
    '''
    for asmt_guid, data in real_data_objects.items():
        if asmt_guid == single_file_key:
            output_file = os.path.join(file_path, LANDING_ZONE_SINGLE_FILE)
            create_csv(data, output_file)
        else:
            filename = LANDING_ZONE_FILE_PATTERN.format(asmt_guid)
            output_file = os.path.join(file_path, filename)
            create_csv(data, output_file)


def get_file_path_from_output_dict(output_dict):
    '''
    '''
    return os.path.dirname(list(output_dict.values())[0])


def add_student_realdata_to_dict(student_realdata_list, real_data_dict, single_file_key, single_file=True):
    '''
    Given a list of students and the realdata dictionary. Place students in the correct bucket of for their assessment.
    If single file is true, place all students in the same bucket
    @param student_realdata_list: The current list of students to place in the dictionary
    @param real_data_dict: The dictionary containing mappings from assessments to lists of students
    @param single_file_key: the key to use when single_file is true
    @param single_file: Whether or not to write all data to a single file
    '''

    if single_file:
        # real_data_dict[single_file_key] = real_data_dict.get(single_file_key, []) + student_realdata_list -- VERY SLOW
        if real_data_dict.get(single_file_key):
            real_data_dict[single_file_key].extend(student_realdata_list)
        else:
            real_data_dict[single_file_key] = student_realdata_list
    else:
        # real_data_dict[rd_record.guid_asmt] = real_data_dict.get(rd_record.guid_asmt, []) + [rd_record] -- SLOW
        for rd_record in student_realdata_list:
            if real_data_dict.get(rd_record.guid_asmt):
                real_data_dict[rd_record.guid_asmt].append(rd_record)
            else:
                real_data_dict[rd_record.guid_asmt] = [rd_record]
    return real_data_dict


def prepare_lz_csv_file(entity_to_path_dict, assessments, single_file):
    '''
    Erase each csv file and then add appropriate header

    @type entity_to_path_dict: dict
    @param entity_to_path_dict: Each key is an entity's class, and each value is the path to its csv file
    '''
    path = get_file_path_from_output_dict(entity_to_path_dict)
    if single_file:
        file_path = os.path.join(path, LANDING_ZONE_SINGLE_FILE)
        prepare_csv_files({RealDataFormat: file_path})
    else:
        for asmt in assessments:
            file_path = os.path.join(path, LANDING_ZONE_FILE_PATTERN.format(asmt.asmt_guid))
            prepare_csv_files({RealDataFormat: file_path})


def create_realdata_objs_from_helper_entities(state_population, school, student_info):
    '''
    '''
    realdata = []
    for subject in student_info.asmt_scores:
        asmt_score_obj = student_info.asmt_scores[subject]
        date_taken = student_info.asmt_dates_taken[subject]
        claim_scores = asmt_score_obj.claim_scores
        #teacher = student_info.teachers[subject]
        params = {
            'guid_asmt': student_info.asmt_guids[subject],
            'guid_asmt_location': school.school_guid,
            'name_asmt_location': school.school_name,
            'grade_asmt': student_info.grade,
            'name_state': state_population.state_name,
            'code_state': state_population.state_code,
            'guid_district': school.district_guid,
            'name_district': school.district_name,
            'guid_school': school.school_guid,
            'name_school': school.school_name,
            'type_school': school.school_category,
            'guid_student': student_info.student_guid,
            'name_student_first': student_info.first_name,
            'name_student_middle': student_info.middle_name,
            'name_student_last': student_info.last_name,
            'address_student_line1': student_info.address_1,
            'address_student_line2': student_info.address_2,
            'address_student_city': student_info.city,
            'address_student_zip': student_info.zip_code,
            'gender_student': student_info.gender,
            'email_student': student_info.email,
            'dob_student': student_info.dob,
            'grade_enrolled': student_info.grade,
            'date_assessed': date_taken.strftime('%Y%m%d'),
            'score_asmt': asmt_score_obj.overall_score,
            'score_asmt_min': asmt_score_obj.interval_min,
            'score_asmt_max': asmt_score_obj.interval_max,
            'score_perf_level': asmt_score_obj.perf_lvl,
            'score_claim_1': claim_scores[0].claim_score,
            'score_claim_1_min': claim_scores[0].claim_score_interval_minimum,
            'score_claim_1_max': claim_scores[0].claim_score_interval_maximum,
            'asmt_claim_1_perf_lvl': claim_scores[0].perf_lvl,
            'score_claim_2': claim_scores[1].claim_score,
            'score_claim_2_min': claim_scores[1].claim_score_interval_minimum,
            'score_claim_2_max': claim_scores[1].claim_score_interval_maximum,
            'asmt_claim_2_perf_lvl': claim_scores[1].perf_lvl,
            'score_claim_3': claim_scores[2].claim_score,
            'score_claim_3_min': claim_scores[2].claim_score_interval_minimum,
            'score_claim_3_max': claim_scores[2].claim_score_interval_maximum,
            'asmt_claim_3_perf_lvl': claim_scores[2].perf_lvl,
            'score_claim_4': claim_scores[3].claim_score if len(claim_scores) > 3 else None,
            'score_claim_4_min': claim_scores[3].claim_score_interval_minimum if len(claim_scores) > 3 else None,
            'score_claim_4_max': claim_scores[3].claim_score_interval_maximum if len(claim_scores) > 3 else None,
            'asmt_claim_4_perf_lvl': claim_scores[3].perf_lvl if len(claim_scores) > 3 else None,
            'dmg_eth_hsp': student_info.dmg_eth_hsp,
            'dmg_eth_ami': student_info.dmg_eth_ami,
            'dmg_eth_asn': student_info.dmg_eth_asn,
            'dmg_eth_blk': student_info.dmg_eth_blk,
            'dmg_eth_pcf': student_info.dmg_eth_pcf,
            'dmg_eth_wht': student_info.dmg_eth_wht,
            'dmg_prg_iep': student_info.dmg_prg_iep,
            'dmg_prg_lep': student_info.dmg_prg_lep,
            'dmg_prg_504': student_info.dmg_prg_504,
            'dmg_prg_tt1': student_info.dmg_prg_tt1,
            #'guid_staff': student_info.teacher_guids[subject],
            #'name_staff_first': teacher.first_name,
            #'name_staff_middle': teacher.middle_name,
            #'name_staff_last': teacher.last_name,
            #'type_staff': 'Teacher',
            'asmt_type': student_info.asmt_types[subject],
            'asmt_year': student_info.asmt_years[subject],
            'asmt_subject': student_info.asmt_subjects[subject],
        }

        realdata.append(RealDataFormat(**params))
    return realdata


def create_helper_entities_from_lz_dict(lz_dict):
    """

    :param lz_dict:
    :return:
    """
    state_params = {
        'state_name': lz_dict['name_state'],
        'state_code': lz_dict['code_state'],
    }
    state = State(**state_params)
    school_params = {
        'school_guid': lz_dict['guid_school'],
        'school_name': lz_dict['name_school'],
        'district_guid': lz_dict['guid_district'],
        'district_name': lz_dict['name_district'],
        'school_category': lz_dict['type_school'],
        'grade_performance_level_counts': None,
    }
    school = School(**school_params)

    teach_params = {
        'first_name': None,
        'middle_name': None,
        'last_name': None,
        'section_guid': None,
        'hier_user_type': None,
        'state_code': None,
        'district_guid': None,
        'school_guid': None,
        'from_date': None,
        'most_recent': None,
        'staff_rec_id': None,
        'staff_guid': None,
    }
    #teacher = Staff(**teach_params)
    subject = lz_dict['asmt_subject']
    claim_score_params = [
        {
            'claim_score': lz_dict['score_claim_1'],
            'claim_score_interval_minimum': lz_dict['score_claim_1_min'],
            'claim_score_interval_maximum': lz_dict['score_claim_1_max'],
            'perf_lvl': lz_dict['asmt_claim_1_perf_lvl']
        },
        {
            'claim_score': lz_dict['score_claim_2'],
            'claim_score_interval_minimum': lz_dict['score_claim_2_min'],
            'claim_score_interval_maximum': lz_dict['score_claim_2_max'],
            'perf_lvl': lz_dict['asmt_claim_2_perf_lvl']
        },
        {
            'claim_score': lz_dict['score_claim_3'],
            'claim_score_interval_minimum': lz_dict['score_claim_3_min'],
            'claim_score_interval_maximum': lz_dict['score_claim_3_max'],
            'perf_lvl': lz_dict['asmt_claim_3_perf_lvl']
        },
        {
            'claim_score': lz_dict['score_claim_4'],
            'claim_score_interval_minimum': lz_dict['score_claim_4_min'],
            'claim_score_interval_maximum': lz_dict['score_claim_4_max'],
            'perf_lvl': lz_dict['asmt_claim_4_perf_lvl']
        },
    ]

    claim_scores = [ClaimScore(**param) for param in claim_score_params]
    asmt_score_params = {
        'overall_score': lz_dict['score_asmt'],
        'interval_min': lz_dict['score_asmt_min'],
        'interval_max': lz_dict['score_asmt_max'],
        'perf_lvl': lz_dict['score_perf_level'],
        'claim_scores': claim_scores,
        'asmt_create_date': None,
    }

    asmt_score = AssessmentScore(**asmt_score_params)

    student_info_params = {
        'grade': lz_dict['grade_asmt'],
        'asmt_guids': {subject: lz_dict['guid_asmt']},
        'student_guid': lz_dict['guid_student'],
        'first_name': lz_dict['name_student_first'],
        'last_name': lz_dict['name_student_last'],
        'middle_name': lz_dict['name_student_middle'],
        'address_1': lz_dict['address_student_line1'],
        'address_2': lz_dict['address_student_line2'],
        'city': lz_dict['address_student_city'],
        'zip_code': lz_dict['address_student_zip'],
        'gender': lz_dict['gender_student'],
        'email': lz_dict['email_student'],
        'dob': lz_dict['dob_student'],
        'asmt_dates_taken': {subject: lz_dict['date_assessed']},
        'dmg_eth_hsp': lz_dict['dmg_eth_hsp'],
        'dmg_eth_ami': lz_dict['dmg_eth_ami'],
        'dmg_eth_asn': lz_dict['dmg_eth_asn'],
        'dmg_eth_blk': lz_dict['dmg_eth_blk'],
        'dmg_eth_pcf': lz_dict['dmg_eth_pcf'],
        'dmg_eth_wht': lz_dict['dmg_eth_wht'],
        'dmg_prg_iep': lz_dict['dmg_prg_iep'],
        'dmg_prg_lep': lz_dict['dmg_prg_lep'],
        'dmg_prg_504': lz_dict['dmg_prg_504'],
        'dmg_prg_tt1': lz_dict['dmg_prg_tt1'],
        'teacher_guids': {subject: None},
        'teachers': {subject: None},
        'asmt_types': {subject: lz_dict['asmt_type']},
        'asmt_years': {subject: lz_dict['asmt_year']},
        'asmt_subjects': {subject: subject},
        'asmt_scores': {subject: asmt_score},
    }

    student_info = StudentInfo(**student_info_params)

    return student_info, state, school


class RealDataFormat(object):
    '''
    An object for holding the real data output format for the UDL pipeline.
    '''
    def __init__(self, guid_asmt, guid_asmt_location, name_asmt_location, grade_asmt, name_state, code_state, guid_district,
                 name_district, guid_school, name_school, type_school, guid_student, name_student_first, name_student_middle,
                 name_student_last, address_student_line1, address_student_line2, address_student_city, address_student_zip, gender_student,
                 email_student, dob_student, grade_enrolled, date_assessed, score_asmt, score_asmt_min, score_asmt_max, score_perf_level,
                 score_claim_1, score_claim_1_min, score_claim_1_max, asmt_claim_1_perf_lvl, score_claim_2, score_claim_2_min, score_claim_2_max,
                 asmt_claim_2_perf_lvl, score_claim_3, score_claim_3_min, score_claim_3_max, asmt_claim_3_perf_lvl, score_claim_4, score_claim_4_min,
                 score_claim_4_max, asmt_claim_4_perf_lvl, dmg_eth_hsp, dmg_eth_ami, dmg_eth_asn, dmg_eth_blk, dmg_eth_pcf, dmg_eth_wht, dmg_prg_iep,
                 dmg_prg_lep, dmg_prg_504, dmg_prg_tt1,
                 # guid_staff, name_staff_first, name_staff_middle, name_staff_last, type_staff,
                 asmt_type, asmt_year, asmt_subject):

        self.guid_asmt = guid_asmt
        self.guid_asmt_location = guid_asmt_location
        self.name_asmt_location = name_asmt_location
        self.grade_asmt = grade_asmt
        self.name_state = name_state
        self.code_state = code_state
        self.guid_district = guid_district
        self.name_district = name_district
        self.guid_school = guid_school
        self.name_school = name_school
        self.type_school = type_school
        self.guid_student = guid_student
        self.name_student_first = name_student_first
        self.name_student_middle = name_student_middle
        self.name_student_last = name_student_last
        self.address_student_line1 = address_student_line1
        self.address_student_line2 = address_student_line2
        self.address_student_city = address_student_city
        self.address_student_zip = address_student_zip
        self.gender_student = gender_student
        self.email_student = email_student
        self.dob_student = dob_student
        self.grade_enrolled = grade_enrolled
        self.date_assessed = date_assessed
        self.score_asmt = score_asmt
        self.score_asmt_min = score_asmt_min
        self.score_asmt_max = score_asmt_max
        self.score_perf_level = score_perf_level
        self.score_claim_1 = score_claim_1
        self.score_claim_1_min = score_claim_1_min
        self.score_claim_1_max = score_claim_1_max
        self.asmt_claim_1_perf_lvl = asmt_claim_1_perf_lvl
        self.score_claim_2 = score_claim_2
        self.score_claim_2_min = score_claim_2_min
        self.score_claim_2_max = score_claim_2_max
        self.asmt_claim_2_perf_lvl = asmt_claim_2_perf_lvl
        self.score_claim_3 = score_claim_3
        self.score_claim_3_min = score_claim_3_min
        self.score_claim_3_max = score_claim_3_max
        self.asmt_claim_3_perf_lvl = asmt_claim_3_perf_lvl
        self.score_claim_4 = score_claim_4
        self.score_claim_4_min = score_claim_4_min
        self.score_claim_4_max = score_claim_4_max
        self.asmt_claim_4_perf_lvl = asmt_claim_4_perf_lvl
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
        #self.guid_staff = guid_staff
        #self.name_staff_first = name_staff_first
        #self.name_staff_middle = name_staff_middle
        #self.name_staff_last = name_staff_last
        #self.type_staff = type_staff
        self.asmt_type = asmt_type
        self.asmt_year = asmt_year
        self.asmt_subject = asmt_subject

    def getRow(self):
        return [self.guid_asmt, self.guid_asmt_location, self.name_asmt_location, self.grade_asmt, self.name_state, self.code_state, self.guid_district, self.name_district, self.guid_school,
                self.name_school, self.type_school, self.guid_student, self.name_student_first, self.name_student_middle, self.name_student_last, self.address_student_line1, self.address_student_line2,
                self.address_student_city, self.address_student_zip, self.gender_student, self.email_student, self.dob_student, self.grade_enrolled, self.date_assessed, self.score_asmt, self.score_asmt_min,
                self.score_asmt_max, self.score_perf_level, self.score_claim_1, self.score_claim_1_min, self.score_claim_1_max, self.asmt_claim_1_perf_lvl, self.score_claim_2, self.score_claim_2_min,
                self.score_claim_2_max, self.asmt_claim_2_perf_lvl, self.score_claim_3, self.score_claim_3_min, self.score_claim_3_max, self.asmt_claim_3_perf_lvl, self.score_claim_4, self.score_claim_4_min,
                self.score_claim_4_max, self.asmt_claim_4_perf_lvl, self.dmg_eth_hsp, self.dmg_eth_ami, self.dmg_eth_asn, self.dmg_eth_blk,
                self.dmg_eth_pcf, self.dmg_eth_wht, self.dmg_prg_iep, self.dmg_prg_lep, self.dmg_prg_504, self.dmg_prg_tt1,
                #self.guid_staff, self.name_staff_first, self.name_staff_middle, self.name_staff_last, self.type_staff,
                self.asmt_type, self.asmt_year, self.asmt_subject]

    @classmethod
    def getHeader(cls):
        return ['guid_asmt', 'guid_asmt_location', 'name_asmt_location', 'grade_asmt', 'name_state', 'code_state', 'guid_district', 'name_district', 'guid_school',
                'name_school', 'type_school', 'guid_student', 'name_student_first', 'name_student_middle', 'name_student_last', 'address_student_line1', 'address_student_line2',
                'address_student_city', 'address_student_zip', 'gender_student', 'email_student', 'dob_student', 'grade_enrolled', 'date_assessed', 'score_asmt', 'score_asmt_min',
                'score_asmt_max', 'score_perf_level', 'score_claim_1', 'score_claim_1_min', 'score_claim_1_max', 'asmt_claim_1_perf_lvl', 'score_claim_2', 'score_claim_2_min', 'score_claim_2_max',
                'asmt_claim_2_perf_lvl', 'score_claim_3', 'score_claim_3_min', 'score_claim_3_max', 'asmt_claim_3_perf_lvl', 'score_claim_4', 'score_claim_4_min',
                'score_claim_4_max', 'asmt_claim_4_perf_lvl', 'dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk',
                'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1',
                #'guid_staff', 'name_staff_first', 'name_staff_middle', 'name_staff_last', 'type_staff',
                'asmt_type', 'asmt_year', 'asmt_subject']
