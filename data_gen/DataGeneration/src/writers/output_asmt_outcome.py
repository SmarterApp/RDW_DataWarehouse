__author__ = 'swimberly'
import csv
import os
from datetime import date

from DataGeneration.src.utils.idgen import IdGen
from DataGeneration.src.models.landing_zone_data_format import output_generated_asmts_to_json, get_file_path_from_output_dict

CSV_K = 'csv'
JSON_K = 'json'
CSV_BY_ID_K = 'csv_by_asmt_id'
PATH_TO_JSON = 'path_to_json_mapping'


def initialize_csv_file(output_config, output_path, output_keys=None):
    """
    Given the output configuration dictionary create the corresponding csv files
    :param output_config: A dictionary of configuration information
    :param output_keys: A list of output formats that should be initialized
        these strings must be the top level keys in the output config dictionary
    :return: a dictionary of output files
    """
    output_files = {}
    output_keys = output_keys if output_keys else output_config.keys()

    for out_key in output_keys:
        csv_info = output_config[out_key].get(CSV_K)
        for table in csv_info:
            file_name = os.path.join(output_path, table + '.csv')
            output_files[table] = file_name
            columns = list(csv_info[table].keys())
            with open(file_name, 'w') as fp:
                csv_writer = csv.writer(fp)
                csv_writer.writerow(columns)

    return output_files


def output_from_dict_of_lists(output_dictionary):
    """
    Given a dictionary where the keys are the output path and the values are lists of dicts corresponding directly
    to the csv file headers, write the rows to file
    :param output_dictionary: dict of the form - {'<file_path>': [row_dict_1, row_dict_2, ...], ...}
    :return: None
    """

    for file_path, list_of_dicts in output_dictionary.items():
        write_csv_rows(file_path, list_of_dicts)


def output_data(output_config, output_files, output_keys=None, school=None, student_info=None, state_population=None,
                inst_hier=None, batch_guid=None, section=None, assessment=None, staff=None, write_data=True):
    """
    Output the data to using the configuration information and the relevant objects
        Works on the assumption that the assessment data is written first
    :param output_config: The output configuration dictionary
    :param output_keys: A list of output formats that should be output from the given data
    :param output_files: A dictionary of output paths for each table to be output
    :param state_population: The state population object to use in outputting data
    :param school: The school object to use in outputting data
    :param student_info: the student info object to use to in outputting data
    :return: A dictionary containing a list of all the objects created mapped to their respective file names
    """

    output_keys = output_keys if output_keys else output_config.keys()
    output_data_dict = {}

    for o_key in output_keys:
        csv_conf = output_config[o_key].get(CSV_K, [])
        json_conf = output_config[o_key].get(JSON_K)
        csv_by_id = output_config[o_key].get(CSV_BY_ID_K, [])

        if json_conf and assessment:
            params = [[assessment], output_files]
            path_to_json = json_conf[PATH_TO_JSON]
            params.append(path_to_json) if os.path.isfile(path_to_json) else None
            output_generated_asmts_to_json(*params)

        # works on the assumption that the assessment data is written first
        if csv_by_id and assessment:
            output_path = get_file_path_from_output_dict(output_files)
            for table in csv_by_id:
                table_out_name = table + '_' + str(assessment.asmt_guid)
                table_out_conf = {'table_out': {CSV_K: {table_out_name: csv_by_id[table]}}}
                path_dict = initialize_csv_file(table_out_conf, output_path, ['table_out'])
                output_files.update(path_dict)
                csv_conf[table_out_name] = csv_by_id[table]

        for table in csv_conf:

            output_file = output_files[table]
            output_data_dict[output_file] = []

            output_data_list = []

            # if student info is present loop on the available subjects to get data
            if student_info:
                for asmt_guid in student_info.asmt_scores:
                    # check that the asmt_guid and the asmt guid for the file match. If not continue
                    if csv_by_id and str(asmt_guid) not in output_file:
                        continue
                    output_row = create_output_csv_dict(csv_conf[table], state_population, school,
                                                        student_info, asmt_guid, inst_hier, batch_guid, section, assessment, staff)
                    output_data_list.append(output_row) if output_row else None

            # otherwise data is not bound by a subject
            else:
                output_row = create_output_csv_dict(csv_conf[table], state_population, school,
                                                    student_info, None, inst_hier, batch_guid, section, assessment, staff)
                output_data_list.append(output_row) if output_row else None

            # if param for writing data is present write rows, otherwise, just return the data.
            if write_data:
                write_csv_rows(output_file, output_data_list)

            # add new data to list for that file in the dictionary
            output_data_dict[output_file] += output_data_list

    return output_data_dict


def create_output_csv_dict(table_config_dict, state_population, school, student_info, asmt_guid, inst_hier, batch_guid, section, assessment, staff):
    """
    Create the csv output dictionary from the given data
    :param table_config_dict: the config dict pertaining directly to the table being output
    :param state_population: The state population object to use in outputting data
    :param school: The school object to use in outputting data
    :param student_info: the student info object to use to in outputting data
    :param subject: the name of the subject to output
    :return: a mapping between column names and values
    """

    output_dict = {}
    idgen = IdGen()

    asmt_score = student_info.asmt_scores[asmt_guid] if student_info else None
    subject = student_info.asmt_subjects[asmt_guid] if student_info else None
    claim_scores = asmt_score.claim_scores if asmt_score else None

    obj_name_map = {
        'student_info': student_info,
        'school': school,
        'state': state_population,
        'state_population': state_population,
        'claim_scores': claim_scores,
        'asmt_scores': asmt_score,
        'asmt_score': asmt_score,
        'asmt_score_obj': asmt_score,
        'date_taken': student_info.asmt_dates_taken[asmt_guid] if student_info else None,
        'inst_hierarchy': inst_hier,
        'batch_guid': MakeTemp(value=batch_guid),
        'idgen': idgen,
        'UNIQUE_ID': MakeTemp(value=idgen.get_id),
        'section': section,
        'assessment': assessment,
        'staff': staff,
        'external_user_student': None,
    }

    required_objects = {obj_name.split('.')[0] for obj_name in table_config_dict.values()}

    # if a required object is missing then this table is not meant to be written or there is an error
    # Return None
    for req_obj in required_objects:
        # if the name we are looking for is not present, that value will be used for the column during output
        if obj_name_map.get(req_obj, not None) is None:
            return None

    for column_name in table_config_dict:
        internal_map_string_list = table_config_dict[column_name].split('.')

        obj_name = internal_map_string_list[0]

        data_object = obj_name_map.get(obj_name, MakeTemp(value=obj_name))

        internal_map_string_list = ['value', 'value'] if isinstance(data_object, MakeTemp) else internal_map_string_list

        # remove everything before the first '.' from attribute name
        attribute_name = '.'.join(internal_map_string_list[1:])

        value = get_value_from_object(data_object, attribute_name, subject, asmt_guid)
        output_dict[column_name] = value

    return output_dict


def get_value_from_object(data_object, attr_name, subject, asmt_guid):
    """
    Using the data object get the value desired and return
    :param data_object: the data object to pull the data from. (could also be a list)
    :param attr_name: Name of the desired attribute
    :param subject: The current subject
    :return: a single cleaned value
    """
    index_attr_list = attr_name.split('.')
    if len(index_attr_list) > 1:
        attr_index, attr_name = index_attr_list
        attr_index = int(attr_index)
        value_list = data_object[attr_index - 1] if len(data_object) > attr_index - 1 else None
        value = getattr(value_list, attr_name) if value_list else None
    else:
        value = getattr(data_object, attr_name)

    # Final value cleanup #
    # if the value is a dictionary, there is a value for each subject
    if isinstance(value, dict):
        value = value.get(asmt_guid) if value.get(asmt_guid) else value.get(subject)

    # if the value is a date object reformat the value
    value = value.strftime('%Y%m%d') if isinstance(value, date) else value
    # check to see if the value is a callable function
    value = value() if callable(value) else value

    return value


def write_csv_rows(output_path, row_dict_list):
    """
    Write the given list of csv dictionaries to the given file
    :param output_path: the path to the output file
    :param row_dict_list: a list of csv dictionaries
    :return: None
    """
    # may want to pass this value in as a parameter or pull this information
    # from the config file if ordering is to be preserved
    fieldnames = get_header_from_file(output_path)
    with open(output_path, 'a') as fp:
        csv_writer = csv.DictWriter(fp, fieldnames)
        csv_writer.writerows(row_dict_list)


def get_header_from_file(filename):
    """
    Open a csv file and return the first row
    :param filename:
    :return: the header as a list
    """
    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        header = next(reader)
    return header


class MakeTemp(object):
    def __init__(self, **kwargs):
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])

if __name__ == '__main__':
    conf_dict = {
        'lz': {
            'csv': {
                'REALDATA': {
                    'guid_asmt': 'student_info.asmt_guids',
                    'guid_asmt_location': 'school.school_guid',
                    'name_asmt_location': 'school.school_name',
                    'grade_asmt': 'student_info.grade',
                    'name_state': 'state_population.state_name',
                    'code_state': 'state_population.state_code',
                    'guid_district': 'school.district_guid',
                    'name_district': 'school.district_name',
                    'guid_school': 'school.school_guid',
                    'name_school': 'school.school_name',
                    'type_school': 'school.school_category',
                    'guid_student': 'student_info.student_guid',
                    'name_student_first': 'student_info.first_name',
                    'name_student_middle': 'student_info.middle_name',
                    'name_student_last': 'student_info.last_name',
                    'address_student_line1': 'student_info.address_1',
                    'address_student_line2': 'student_info.address_2',
                    'address_student_city': 'student_info.city',
                    'address_student_zip': 'student_info.zip_code',
                    'gender_student': 'student_info.gender',
                    'email_student': 'student_info.email',
                    'dob_student': 'student_info.dob',
                    'grade_enrolled': 'student_info.grade',
                    'score_claim_1': 'claim_scores.1.claim_score',
                    'score_claim_2': 'claim_scores.2.claim_score',
                    'score_claim_3': 'claim_scores.3.claim_score',
                    'date_taken': 'student_info.asmt_dates_taken',
                }
            }
        }
    }

    out_keys = ['lz']
    out_path = os.getcwd()
    out_files = initialize_csv_file(conf_dict, out_keys, out_path)
    print(out_files)
    student_info1 = MakeTemp(asmt_guids=1, student_guid=2, first_name='bill', last_name='nye', middle_name='tom',
                             address_1='1 bob st.', address_2='', city='North Carolina', zip_code=12345, gender='m',
                             email='b.n@email.com', dob='11111999', grade=4, asmt_dates_taken=date.today(),
                             asmt_scores={'math': MakeTemp(claim_scores=[MakeTemp(claim_score=1200), MakeTemp(claim_score=1200),
                                                                         MakeTemp(claim_score=1200), MakeTemp(claim_score=1200)]),
                                          'ela': MakeTemp(claim_scores=[MakeTemp(claim_score=1300), MakeTemp(claim_score=1300),
                                                                        MakeTemp(claim_score=1300)])})
    state1 = MakeTemp(state_name='North Carolina', state_code="NC")
    school1 = MakeTemp(school_guid=123, school_name='school123', district_name='district1', district_guid='d123',
                       school_category='elementary')
    output_data(conf_dict, out_keys, out_files, school1, student_info1, state1)
