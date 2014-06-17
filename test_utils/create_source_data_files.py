"""
Created on May 7, 2014

@author: nestep
"""

import argparse
import configparser
import csv
import os
import random
import uuid

from sqlalchemy import and_, select
import xml.etree.cElementTree as ET
from edcore.database import get_data_source_names, initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection
from edschema.database.connector import DBConnection


def main(config_file, tenant_to_update, out_dir, verbose, raw, item):
    """
    Imports data from csv
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    initialize_db(EdCoreDBConnection, config['app:main'])
    for tenant in get_data_source_names():
        if tenant_to_update in tenant:
            # Get necessary meta-data
            state_code = get_state_code(tenant)
            assessments = get_all_assessments(tenant)

            if item:
                # Create item pools for each assessment
                create_item_pools(assessments)

            # Build files for each assessment
            for asmt in assessments:
                students = get_students_for_assessment(tenant, asmt['guid'])
                generate_data_files(out_dir, state_code, asmt, students, verbose, raw, item)


def get_state_code(tenant):
    """Get the state code in FAO"""
    with DBConnection(tenant) as connection:
        fact_asmt = connection.get_table("fact_asmt_outcome_vw")
        query = select([fact_asmt.c.state_code], from_obj=[fact_asmt]).limit(1)
        results = connection.get_result(query)

        for result in results:
            return result['state_code']


def get_all_assessments(tenant):
    """Get all unique assessments"""
    with DBConnection(tenant) as connection:
        dim_asmt = connection.get_table("dim_asmt")
        query = select([dim_asmt.c.asmt_guid, dim_asmt.c.asmt_period_year, dim_asmt.c.asmt_type,
                        dim_asmt.c.effective_date, dim_asmt.c.asmt_subject], from_obj=dim_asmt)
        results = connection.get_result(query)

        asmts = []
        for result in results:
            asmts.append({'guid': result['asmt_guid'], 'year': result['asmt_period_year'], 'type': result['asmt_type'],
                          'effective_date': result['effective_date'], 'subject': result['asmt_subject']})

    return asmts


def create_item_pools(assessments):
    """Create item pools for each assessment"""
    for asmt in assessments:
        pool = []
        for _ in range(200):
            pool.append({'key': uuid.uuid4(), 'client': uuid.uuid4(),
                         'type': random.choice(['MC', 'MS', 'graphicGapMatchInteraction', 'EQ']),
                         'segment': '(SBAC)SBAC-MG110PT-S3-' + str(asmt['subject']).upper()})
        asmt['item_pool'] = pool


def get_students_for_assessment(tenant, asmt_guid):
    """Get all students who have records for a given assessment"""
    with DBConnection(tenant) as connection:
        fact_asmt = connection.get_table("fact_asmt_outcome_vw")
        query = select([fact_asmt.c.student_guid, fact_asmt.c.asmt_grade, fact_asmt.c.district_guid],
                       from_obj=fact_asmt).where(and_(fact_asmt.c.asmt_guid == asmt_guid))
        results = connection.get_result(query)

        students = []
        for result in results:
            students.append({'guid': result['student_guid'], 'district_guid': result['district_guid'],
                             'grade': result['asmt_grade']})

    return students


def generate_data_files(root_dir, state_code, asmt, students, verbose, raw, item):
    """Generate item-level files"""
    for student in students:
        # Build directory path and file name
        dir_path = os.path.join(root_dir, str(state_code).upper(), str(asmt['year']),
                                str(asmt['type']).upper().replace(' ', '_'), str(asmt['effective_date']),
                                str(asmt['subject']).upper(), str(student['grade']), str(student['district_guid']))

        # Make sure directory exists
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if item:
            # Select items from the pool
            items = random.sample(asmt['item_pool'], 100)
            # Create file
            item_file_name = (str(student['guid']) + '.csv')
            item_file_path = os.path.join(dir_path, item_file_name)
            with open(item_file_path, 'w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for i in range(100):
                    item = items[i]
                    csv_writer.writerow([item['key'], student['guid'], item['segment'], i, item['client'], 1, 1,
                                         item['type'], 0, 1, '2013-04-03T16:21:33.660', 1, 'MA-Undesignated',
                                         'MA-Undesignated', 1, 1, 1, 0])
            if verbose:
                print(os.path.join(dir_path, item_file_name))
        if raw:
            raw_file_name = (str(student['guid']) + '.xml')
            raw_file_path = os.path.join(dir_path, raw_file_name)
            with open(raw_file_path, 'w') as xml_file:
                root = ET.Element("root")
                student_node = ET.SubElement(root, "student")
                student_node.set("guid", str(student['guid']))
                tree = ET.ElementTree(root)
                tree.write(raw_file_path)
            if verbose:
                print(os.path.join(dir_path, raw_file_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Item level CSV/Source Raw XML')
    parser.add_argument('-i', '--item', help='Item level CSV data', action='store_true', default=False)
    parser.add_argument('-r', '--raw', help='Raw XML data', action='store_true', default=False)
    parser.add_argument('-c', '--config', help='Set the path to ini file')
    parser.add_argument('-t', '--tenant', help='Tenant to import data to', default='cat')
    parser.add_argument('-o', '--outDir', help='Root directory to place files')
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true', default=False)
    args = parser.parse_args()

    __raw = args.raw
    __item = args.item
    __config = args.config
    __tenant = args.tenant
    __out_dir = args.outDir
    __verbose = args.verbose

    if __out_dir is None:
        __out_dir = '/opt/edware/item_level' if __item else '/opt/edware/raw_data' if __raw else None

    if not __raw and not __item:
        raise argparse.ArgumentError('--raw or --item option needed')

    parent_dir = os.path.abspath(os.path.join('..', os.path.dirname(__file__)))

    if __config is None:
        __config = os.path.join(os.path.join(parent_dir, 'smarter'), 'test.ini')

    if os.path.exists(__config) is False:
        print('Error: config file does not exist')
        exit(-1)

    main(__config, __tenant, __out_dir, __verbose, __raw, __item)
