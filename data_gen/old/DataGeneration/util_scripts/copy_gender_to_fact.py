'''
Created on Aug 27, 2013

@author: swimberly

copy_gender_to_fact.py
Script to read in a dim_student and a fact_asmt_outcome csv file where the
fact_asmt_outcome file does not have the gender column populated.
Output a separate file where the column is populated.
'''

import csv
import argparse


def read_student_file(filename):
    '''
    Read the dim_student file and create a dictionary where each student guid
    maps to their gender
    '''
    with open(filename, 'r') as csv_file:
        creader = csv.DictReader(csv_file)
        student_dict = {}
        for row in creader:
            student_dict[row['student_id']] = row['gender']

    return student_dict


def read_write_fact(fact_file, output_file, student_dict):
    '''
    Read a row from fact assessment. Find the student's gender in the student dict.
    Write a row to the output file where the gender has been populated
    '''
    with open(fact_file, 'r') as fact_csv:
        with open(output_file, 'w') as out_csv:
            fact_reader = csv.reader(fact_csv)
            out_writer = csv.writer(out_csv)

            header = next(fact_reader)
            out_writer.writerow(header)
            student_id_index = header.index('student_id')
            gender_index = header.index('gender')

            for row in fact_reader:
                student_id = row[student_id_index]
                student_gender = student_dict[student_id]
                out_row = row[:]
                out_row[gender_index] = student_gender
                out_writer.writerow(out_row)


def main(fact_file, student_file, output_file):
    if fact_file == output_file:
        exit('please specify a different location or name for the output file')
    student_gender_dict = read_student_file(student_file)
    read_write_fact(fact_file, output_file, student_gender_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Take a fact asmt file without gender and make a copy that has a populated gender column')
    parser.add_argument('-f', '--fact-file', help='the location of the fact_asmt_outcome.csv file')
    parser.add_argument('-s', '--student-file', help='the dim_student.csv file')
    parser.add_argument('-o', '--output-file', help='the location and name of the output file')
    args = parser.parse_args()

    main(args.fact_file, args.student_file, args.output_file)
