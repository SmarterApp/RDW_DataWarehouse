import os
import logging
import csv
from pyramid.threadlocal import get_current_registry
from smarter_score_batcher.tasks.remote_file_writer import remote_write
from smarter_score_batcher.tasks.remote_csv_writer import remote_csv_generator
from smarter_score_batcher.utils.csv_utils import get_all_elements_for_tsb_csv
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper
from smarter_score_batcher.utils.xml_utils import extract_meta_without_fallback_helper
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from edcore.utils.file_utils import generate_path_to_raw_xml
from edcore.utils.file_utils import generate_path_to_item_csv

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")

DEFAULT_VALUE = 'NA'
ATTRIBUTE_CONTEXT_VALUE_FINAL = 'FINAL'
ATTRIBUTE_CONTEXT_VALUE_INITIAL = 'INITIAL'


class Meta:
    def __init__(self, valid_meta, student_id, state_code, district_id, academic_year, asmt_type, subject, grade, effective_date):
        self.__student_id = student_id
        self.__state_code = state_code
        self.__district_id = district_id
        self.__academic_year = academic_year
        self.__asmt_type = asmt_type
        self.__grade = grade
        self.__subject = subject
        self.__effective_date = effective_date
        self.__valid_meta = valid_meta

    @property
    def student_id(self):
        return self.__student_id

    @property
    def state_code(self):
        return self.__state_code

    @property
    def district_id(self):
        return self.__district_id

    @property
    def academic_year(self):
        return self.__academic_year

    @property
    def asmt_type(self):
        return self.__asmt_type

    @property
    def grade(self):
        return self.__grade

    @property
    def subject(self):
        return self.__subject

    @property
    def effective_date(self):
        return self.__effective_date

    @property
    def valid_meta(self):
        return self.__valid_meta


def process_xml(raw_xml_string):
    ''' Process tdsreport doc
    '''
    meta_names = extract_meta_names(raw_xml_string)
    if not meta_names.valid_meta:
        raise EdApiHTTPPreconditionFailed("Invalid XML")
    settings = get_current_registry().settings
    root_dir = settings.get("smarter_score_batcher.base_dir.xml")
    xml_file_path = create_path(root_dir, meta_names, generate_path_to_raw_xml)
    args = (xml_file_path, raw_xml_string)
    timeout = settings.get("smarter_score_batcher.celery_timeout", 30)
    queue_name = settings.get('smarter_score_batcher.sync_queue')
    celery_response = remote_write.apply_async(args=args, queue=queue_name)
    # wait until file successfully written to disk
    return celery_response.get(timeout=timeout)


def create_csv(raw_xml_string):
    meta_names = extract_meta_names(raw_xml_string)
    settings = get_current_registry().settings
    root_dir_csv = settings.get("smarter_score_batcher.base_dir.csv")
    root_dir_xml = settings.get("smarter_score_batcher.base_dir.xml")
    xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
    csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
    queue_name = settings.get('smarter_score_batcher.sync_queue')
    args = (csv_file_path, xml_file_path)
    celery_response = remote_csv_generator.apply_async(args=args, queue=queue_name)
    return celery_response


def create_path(root_dir, meta, generate_path):
    kwargs = {}
    kwargs['state_code'] = meta.state_code
    kwargs['asmt_year'] = meta.academic_year
    kwargs['asmt_type'] = meta.asmt_type
    kwargs['effective_date'] = meta.effective_date
    kwargs['asmt_subject'] = meta.subject
    kwargs['asmt_grade'] = meta.grade
    kwargs['district_id'] = meta.district_id
    kwargs['student_id'] = meta.student_id
    path = generate_path(root_dir, **kwargs)
    return path


def extract_meta_names(raw_xml_string):
    '''Validates and extracts meta from the XML.
    Returns: True if meta for file path is valid. And the parts for folder creation.
    '''
    try:
        root = ET.fromstring(raw_xml_string)
        #state_code -> StateName for now
        state_code = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeRelationship/[@name='StateName']", "value", "context")
        student_id = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='SSID']", "value", "context")
        district_id = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeRelationship/[@name='DistrictID']", "value", "context")
        academic_year = extract_meta_without_fallback_helper(root, "./Test", "academicYear")
        asmt_type = extract_meta_without_fallback_helper(root, "./Test", "assessmentType")
        subject = extract_meta_without_fallback_helper(root, "./Test", "subject")
        grade = extract_meta_without_fallback_helper(root, "./Test", "grade")
        effective_date = 'NA'  # root.find("./test").get('effectiveDate', DEFAULT_VALUE)
        validMeta = state_code and student_id and district_id and academic_year and asmt_type and subject and grade
        return Meta(validMeta, student_id, state_code, district_id, academic_year, asmt_type, subject, grade, effective_date)
    except ET.ParseError:
        raise EdApiHTTPPreconditionFailed("Invalid XML")
