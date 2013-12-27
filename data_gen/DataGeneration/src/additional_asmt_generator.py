__author__ = 'swimberly'

import os
import argparse
import csv
import json
import datetime
from collections import OrderedDict
import random
import uuid
from time import mktime, strptime

from DataGeneration.src.writers.write_to_csv import create_csv, prepare_csv_files
from DataGeneration.src.models.landing_zone_data_format import (create_helper_entities_from_lz_dict,
                                                                create_realdata_objs_from_helper_entities,
                                                                add_student_realdata_to_dict, RealDataFormat)


ID = 'identification'
TYPE = 'type'
GUID = 'guid'
PERF_LVLS = 'performance_levels'
OVERALL = 'overall'
MIN = 'min_score'
MAX = 'max_score'
CUT_POINT = 'cut_point'
JSON_PATTERN = 'METADATA_ASMT_ID_{}.json'
CSV_PATTERN = 'REALDATA_ASMT_ID_{}.csv'
DATE_TAKEN = 'date_assessed'
DATE_FORMAT = '%Y%m%d'


def update_row(row_dict, perf_change_tup, asmt_type, asmt_dict, json_map, date_change=-3):
    """
    Given a row dictionary for the record to be updated, change the values for the relevant fields and return
    the dictionary
    :param row_dict: A dict object containing the data for the current row to be updated
    :param perf_change_tup: A tuple containing the range of performance change as percentages.
        ie (10, 15) would be 10 to 15 point increase, where (-15, -10) would be 10 to 15 point decrease
    :param asmt_type: The type of assessment that the updated record should be for
    :param asmt_dict: A dictionary mapping the old assessment guids to the new assessment guids
    :param json_map: A dictionary mapping the new assessment guid to the corresponding json assessment data
    :param date_change: the number of months to change the date taken by, default is -3 (3 months previous)
    :return: A dictionary with the values updated properly
    """
    old_asmt_guid = row_dict['guid_asmt']
    json_obj = json_map[asmt_dict[old_asmt_guid]]

    # update the date
    date_object = datetime.date.fromtimestamp(mktime(strptime(row_dict[DATE_TAKEN], DATE_FORMAT)))
    row_dict[DATE_TAKEN] = month_delta(date_object, date_change)

    # update the scores
    cut_points = get_cut_points(json_obj)
    min_score = json_obj[OVERALL][MIN]
    max_score = json_obj[OVERALL][MAX]
    row_dict = update_scores(row_dict, perf_change_tup, cut_points, min_score, max_score)

    # update assessment type and guid
    row_dict['asmt_type'] = asmt_type
    row_dict['guid_asmt'] = asmt_dict[old_asmt_guid]

    return row_dict


def generate_score_offset(perf_change_tup):
    """
    Given a score range tuple generate a random value between the two numbers
    :param perf_change_tup: A tuple containing 2 integers
    :return: A random integer between the two values
    """
    assert isinstance(perf_change_tup[0], int)
    assert isinstance(perf_change_tup[1], int)

    sorted_range = sorted(perf_change_tup)
    offset = random.randint(sorted_range[0], sorted_range[1])
    return offset


def update_scores(row_dict, perf_change_tup, cut_points, min_score, max_score):
    """
    Update the scores in the given assessment outcome record based on the perf_change_tuple
    :param row_dict: A dict object containing the data for the current row to be updated4
    :param perf_change_tup: A tuple containing the range of performance change as percentages.
        ie (10, 15) would be 10 to 15 point increase, where (-15, -10) would be 10 to 15 point decrease
    :param cut_points: a list of ordered values to use as cutpoints (ie. [1400, 1800, 2100])
    :param min_score: the minimum score for the assessment
    :param max_score: the maximum score for the assessment
    :return: the updated row dictionary
    """
    min_score = int(min_score)
    max_score = int(max_score)
    offset = generate_score_offset(perf_change_tup)

    row_dict['score_asmt'] = min(max(int(row_dict['score_asmt']) + offset, min_score), max_score)
    row_dict['score_asmt_min'] = min(max(int(row_dict['score_asmt_min']) + offset, min_score), max_score)
    row_dict['score_asmt_max'] = min(max(int(row_dict['score_asmt_max']) + offset, min_score), max_score)
    row_dict['score_perf_level'] = determine_perf_lvl(row_dict['score_asmt'], cut_points)

    # assessment claim score cut points will divide the assessment score range in to three equal parts
    step = (max_score - min_score)/3
    asmt_claim_score_cut_points = [min_score + step, min_score + (step * 2)]

    # loop over each claim score, break from the loop if there are no more claims
    # or if the value cannot be converted to an int
    i = 0
    while True:
        try:
            offset = generate_score_offset(perf_change_tup)
            row_dict['score_claim_{}'.format(i + 1)] = min(max(int(row_dict['score_claim_{}'.format(i + 1)]) + offset, min_score), max_score)
            row_dict['score_claim_{}_max'.format(i + 1)] = min(max(int(row_dict['score_claim_{}_max'.format(i + 1)]) + offset, min_score), max_score)
            row_dict['score_claim_{}_min'.format(i + 1)] = min(max(int(row_dict['score_claim_{}_min'.format(i + 1)]) + offset, min_score), max_score)
            row_dict['asmt_claim_{}_perf_lvl'.format(i + 1)] = determine_perf_lvl(row_dict['score_claim_{}'.format(i + 1)], asmt_claim_score_cut_points)
        except KeyError:
            break
        except ValueError:
            break
        i += 1

    return row_dict


def get_cut_points(json_dict):
    """
    Get a list of the cut points from the assessment dictionary
    :param json_dict: the dictionary or OrderedDict that is holding the assessment information
    :return: a list of sorted cut points
    """
    min_max_score = [json_dict[OVERALL][MIN], json_dict[OVERALL][MAX]]
    perf_lvl_dict = json_dict[PERF_LVLS]

    return sorted([int(x[CUT_POINT]) for x in perf_lvl_dict.values()
                   if x[CUT_POINT] not in min_max_score and x[CUT_POINT] != ''])


def determine_perf_lvl(score, cut_points):
    """
    Determine the performance level of the score
    :param score: the assessment score
    :param cut_points: A list of cut points that excludes min and max scores
    :return: the performance level
    """
    for i in range(len(cut_points)):
        if score < cut_points[i]:
            return i + 1
    return len(cut_points) + 1


def month_delta(date, delta):
    """
    Given a date object and a month delta, change the date to have an updated month
    :param date: A datetime.date object representing the date you want to change
    :param delta: The number of months you would like to change the date by, either positive or negative
    :return: An updated date object
    """
    m, y = (date.month + delta) % 12, date.year + (date.month + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day,
            [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)


def create_new_json_file(old_json_filename, asmt_type, output_location):
    """
    Create a new json file using the given information
    :param old_json_filename: the name/path of the json filename
    :type old_json_filename: str
    :param asmt_guid: the new asmt_guid to use
    :param asmt_type: the type of the assessment being created
    :return: a tuple containing - the new json dictionary, the old assessment guid, the new assessment guid
    """
    with open(old_json_filename, 'r') as fp:
        json_dict = json.load(fp, object_pairs_hook=OrderedDict)

    new_asmt_guid = str(uuid.uuid4())
    old_asmt_guid = json_dict[ID][GUID]
    json_dict[ID][GUID] = new_asmt_guid
    json_dict[ID][TYPE] = asmt_type

    new_filename = os.path.join(output_location, JSON_PATTERN.format(new_asmt_guid))

    with open(new_filename, 'w') as fp:
        json.dump(json_dict, fp, indent=4)

    return json_dict, old_asmt_guid, new_asmt_guid


def read_csv_file(csv_file_name, perf_change_tup, asmt_type, asmt_dict, date_change, output_path, star_format, json_map, batch_size=100000):
    """
    Read a given csv file and output updated records to a new csv file
    :param csv_file_name: The name and path of the incoming csv file
    :param perf_change_tup: The tuple that list min and max performance change (in points)
    :param asmt_type: The type of assessment to output
    :param asmt_dict: The dictionary mapping old assessment guids to the new assessment guid
    :param date_change: The number of months to change date by
    :param output_path: The location where files should be output
    :param star_format: Whether or not to generate star schema file format
    :param json_map: A dictionary mapping the new assessment guid to the json dictionary
    :param batch_size: The maximum number of records to read before returning
    :return: None
    """

    with open(csv_file_name, 'r') as cf:
        c_creader = csv.DictReader(cf)
        student_list_by_asmt = create_list_of_csv_records(c_creader, batch_size, perf_change_tup, asmt_type, asmt_dict, date_change, json_map)
        while student_list_by_asmt:
            output_data(student_list_by_asmt, output_path, star_format)
            student_list_by_asmt = create_list_of_csv_records(c_creader, batch_size, perf_change_tup, asmt_type, asmt_dict, date_change, json_map)


def create_list_of_csv_records(csv_reader, batch_size, perf_change_tup, asmt_type, asmt_dict, date_change, json_map):
    """
    Create a list of the csv records that should be updated
    :param csv_reader: A csv reader object
    :param batch_size: The maximum number of records to read before returning
    :param perf_change_tup: The tuple that list min and max performance change (in points)
    :param asmt_type: The type of assessment to output
    :param asmt_dict: The dictionary mapping old assessment guids to the new assessment guid
    :param date_change: The number of months to change date by
    :param json_map: A dictionary mapping the new assessment guid to the json dictionary
    :return: A dictionary mapping assessment guids to the corresponding list of student info objects
    """
    student_info_by_asmt = {}

    for i in range(batch_size):
        try:
            row_dict = next(csv_reader)
            updated_row = update_row(row_dict, perf_change_tup, asmt_type, asmt_dict, json_map, date_change)
            student_info, state, school = create_helper_entities_from_lz_dict(updated_row)

            asmt_guid = list(student_info.asmt_guids.values())[0]

            if not student_info_by_asmt.get(asmt_guid):
                # init key inside dict
                student_info_by_asmt[asmt_guid] = []

            student_info_by_asmt[asmt_guid].append((state, school, student_info))
        except StopIteration:
            break

    return student_info_by_asmt


def output_data(student_tup_map, output_path, star_format=False):
    """
    Output student data to landing zone csv file and star format it specified
    header should already be written to file, using prepare_csv()
    :param student_tup_map: a map of lists of tuples of the format:
        {asmt_guid: [(state_obj, school_obj, student_info_object), ...], ...}
    :param output_path:
    :param star_format: Whether to generate the star schema format - NOT IMPLEMENTED
    :return: None
    """

    # Output lz_format
    real_data_dict = {}

    for asmt_guid in student_tup_map:
        for stu_tup in student_tup_map[asmt_guid]:
            read_data_list = create_realdata_objs_from_helper_entities(*stu_tup)
            add_student_realdata_to_dict(read_data_list, real_data_dict, 1, False)

    for asmt_guid, data in real_data_dict.items():
        filename = CSV_PATTERN.format(asmt_guid)
        output_file = os.path.join(output_path, filename)
        create_csv(data, output_file)

    # Output Star format
    if star_format:
        pass


def create_performance_change_tuple(score_change_lo, score_change_hi, positive_change):
    """
    Create a tuple comprised of the score change interval
    :param score_change_lo: Lower bound on score change
    :param score_change_hi: Upper bound on score change
    :param positive_change: If the change should be positive or negative
    :return: A tuple that holds positive or negative versions of the two values
    """
    if positive_change:
        score_change_lo = max(score_change_lo, -score_change_lo)
        score_change_hi = max(score_change_hi, -score_change_hi)
    else:
        score_change_lo = min(score_change_lo, -score_change_lo)
        score_change_hi = min(score_change_hi, -score_change_hi)

    return score_change_lo, score_change_hi


def main(input_csv_list, input_json_list, output_asmt_type, output_dir, month_change, asmt_change_low, asmt_change_hi, positive_change=False, star_format=False):
    """
    Main method for subsequent assessment generation
    :param input_csv_list: A list of csv files to read
    :param input_json_list: A list of json files to read
    :param output_asmt_type: Type of assessment to be output
    :param output_dir: Where to write the output
    :param month_change: How many months to offset the year
    :param asmt_change_low: Lower bound on score change
    :param asmt_change_hi: Upper bound on score change
    :param positive_change: Whether or not the change should be positive
    :param star_format: Whether or not star schema format should be output
    :return: None
    """
    assert isinstance(input_csv_list, list)
    assert isinstance(input_json_list, list)

    asmt_map = {}
    json_map = {}

    #update json file
    for json_file in input_json_list:
        json_dict, old_guid, new_guid = create_new_json_file(json_file, output_asmt_type, output_dir)
        asmt_map[old_guid] = new_guid
        json_map[new_guid] = json_dict

        # prepare output csv file for lz format
        file_path = os.path.join(output_dir, CSV_PATTERN.format(new_guid))
        prepare_csv_files({RealDataFormat: file_path})

    # TODO: prepare output csv file for star format

    perf_change_tup = create_performance_change_tuple(asmt_change_low, asmt_change_hi, positive_change)

    # update csv files
    for csv_file in input_csv_list:
        read_csv_file(csv_file, perf_change_tup, output_asmt_type, asmt_map, month_change, output_dir, star_format, json_map)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script that will read the landing zone file generated for a given"
                                                 "assessment and create (a) new file(s) for another assessment")
    parser.add_argument('-c', '--input-csv', nargs='+', required=True,
                        help='The name of the csv file(s) to use to generate new assessments. '
                             'Supply at least 1 filename')
    parser.add_argument('-j', '--input-json', nargs='+', help='The name of the json file(s) to use to generate new '
                                                              'assessments. Supply at least 1 filename')
    parser.add_argument('-a', '--asmt-type', help='The output assessment type')
    parser.add_argument('--star-format', action='store_true',
                        help='Generate the star schema format in addition to the landing zone format')
    parser.add_argument('-o', '--output-location', default=os.getcwd(),
                        help='The path to the directory where files should be written. Default: current working dir')
    parser.add_argument('-m', '--month-change', default=-3, type=int,
                        help='The number of months to offset the current date of the assessment. Default: -3')
    parser.add_argument('-l', '--score-change-low', type=int, default=30,
                        help='The lower bound on how much to change the assessment scores, default: 30')
    parser.add_argument('-u', '--score-change-high', type=int, default=300,
                        help='The upper bound on how much to change the assessment scores, default: 300')
    parser.add_argument('-p', '--positive-score-change', action='store_true',
                        help='whether score change should be positive or negative')

    args = parser.parse_args()
    print(args)

    main(args.input_csv, args.input_json, args.asmt_type, args.output_location, args.month_change, args.score_change_low,
         args.score_change_high, args.positive_score_change, args.star_format)
