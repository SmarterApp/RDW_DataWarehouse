'''
Created on Sep 23, 2014

@author: tosako
'''
from smarter_score_batcher.error.error_file_generator import build_err_list,\
    generate_error_file
from test.test_xml_etree import ET
from smarter_score_batcher.processing.file_processor import generate_assessment_metadata_file


def handle_error(e_TSBException, err_file_path, xml_file_path, json_file_path):

    err_code = e_TSBException.err_code
    err_source = e_TSBException.err_source
    err_code_text = e_TSBException.err_code_text
    err_source_text = e_TSBException.err_source_text
    err_input = e_TSBException.err_input
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    generate_assessment_metadata_file(root, json_file_path)
    err_list = build_err_list(err_code, err_source, err_code_text, err_source_text, err_input)
    generate_error_file(err_file_path, err_list)
