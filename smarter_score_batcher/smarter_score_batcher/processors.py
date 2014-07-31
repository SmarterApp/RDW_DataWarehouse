import os
from pyramid.threadlocal import get_current_registry
from smarter_score_batcher.tasks.remote_file_writer import remote_write


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

DEFAULT_VALUE = 'NA'
ATTRIBUTE_CONTEXT_VALUE_FINAL = 'FINAL'
ROOT_DIR = '/tmp'


class Meta:
    def __init__(self, student_id, state_name, district_id, academic_year, asmt_type, subject, grade, effective_date):
        self.student_id = student_id
        self.state_name = state_name
        self.district_id = district_id
        self.academic_year = academic_year
        self.asmt_type = asmt_type
        self.grade = grade
        self.subject = subject
        self.effective_date = effective_date


def process_xml(raw_xml_string):
    ''' Process tdsreport doc
    '''
    file_path = parse_file_path(raw_xml_string)
    args = (file_path, raw_xml_string)
    # TODO: may need a separate queue to write xml files ?
    settings = get_current_registry().settings
    timeout = settings.get("smarter_score_batcher.celery_timeout", 30)
    celery_response = remote_write.apply_async(args=args)
    # TODO: wait until writing succeeds
    return celery_response.get(timeout=timeout)


def parse_file_path(args):
    # TODO: raise exception if we cannot parse file path
    return "/tmp/hello/world/test.xml"


def create_path(root_dir, meta):
    path = os.path.join(root_dir, meta.state_name, meta.academic_year, meta.asmt_type, meta.effective_date, meta.subject, meta.grade, meta.district_id)
    os.makedirs(path, exist_ok=True)
    return path


def extract_meta_names(root):
    state_name = [e.get('value', DEFAULT_VALUE) for e in root.findall("./testee/testeerelationship/[@name='StateName']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
    district_id = [e.get('value', DEFAULT_VALUE) for e in root.findall("./testee/testeerelationship/[@name='DistrictID']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
    student_id = [e.get('value', DEFAULT_VALUE) for e in root.findall("./testee/testeeattribute/[@name='SSID']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
    asmt_type = root.find("./test").get('assessmentType', DEFAULT_VALUE)
    subject = root.find("./test").get('subject', DEFAULT_VALUE)
    academic_year = root.find("./test").get('academicYear', DEFAULT_VALUE)
    grade = root.find("./test").get('grade', DEFAULT_VALUE)
    effective_date = 'NA'  # root.find("./test").get('effectiveDate', DEFAULT_VALUE)
    return Meta(student_id, state_name, district_id, academic_year, asmt_type, subject, grade, effective_date)
