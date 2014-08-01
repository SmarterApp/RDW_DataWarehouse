import os, logging
from pyramid.threadlocal import get_current_registry
from smarter_score_batcher.tasks.remote_file_writer import remote_write
from edapi.httpexceptions import EdApiHTTPPreconditionFailed


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")

DEFAULT_VALUE = 'NA'
ATTRIBUTE_CONTEXT_VALUE_FINAL = 'FINAL'
ATTRIBUTE_CONTEXT_VALUE_INITIAL = 'INITIAL'
ROOT_DIR = '/tmp'


class Meta:
    def __init__(self, valid_meta, student_id, state_name, district_id, academic_year, asmt_type, subject, grade, effective_date):
        self.student_id = student_id
        self.state_name = state_name
        self.district_id = district_id
        self.academic_year = academic_year
        self.asmt_type = asmt_type
        self.grade = grade
        self.subject = subject
        self.effective_date = effective_date
        self.valid_meta = valid_meta


def process_xml(raw_xml_string):
    ''' Process tdsreport doc
    '''
    meta_names = extract_meta_names(raw_xml_string)
    if not meta_names.valid_meta:
        raise EdApiHTTPPreconditionFailed("content cannot be empty")
    file_path = create_path(ROOT_DIR, meta_names)
    args = (file_path, raw_xml_string)
    settings = get_current_registry().settings
    timeout = settings.get("smarter_score_batcher.celery_timeout", 30)
    queue_name = settings.get('smarter_score_batcher.sync_queue')
    celery_response = remote_write.apply_async(args=args, queue=queue_name)
    # wait until file successfully written to disk
    return celery_response.get(timeout=timeout)


def create_path(root_dir, meta):
    path = os.path.join(root_dir, meta.state_name, meta.academic_year, meta.asmt_type, meta.effective_date, meta.subject, meta.grade, meta.district_id)
    return path


def extract_meta_names(raw_xml_string):
    '''Validates and extracts meta from the XML.
    Returns: True if meta for file path is valid. And the parts for folder creation.
    '''
    root = ET.fromstring(raw_xml_string)
    state_name, is_state_name_valid = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeRelationship/[@name='StateName']" )
    student_id, is_student_id_valid = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='SSID']" )
    district_id, is_district_id_valid = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeRelationship/[@name='DistrictID']" )
    academic_year, is_academic_year_valid = extract_meta_without_fallback_helper(root, "academicYear")
    asmt_type, is_asmt_type_valid = extract_meta_without_fallback_helper(root, "assessmentType")
    subject, is_subject_valid = extract_meta_without_fallback_helper(root, "subject")
    grade, is_grade_valid = extract_meta_without_fallback_helper(root, "grade")
    effective_date = 'NA'  # root.find("./test").get('effectiveDate', DEFAULT_VALUE)
    validMeta = is_state_name_valid and is_student_id_valid and is_district_id_valid and is_academic_year_valid and is_asmt_type_valid and is_subject_valid and is_grade_valid
    return Meta(validMeta, student_id, state_name, district_id, academic_year, asmt_type, subject, grade, effective_date)


def extract_meta_with_fallback_helper(root, element_xpath):
    valid_meta = True
    if (root.find(element_xpath)) is not None:
        try:
            element = [e.get('value', DEFAULT_VALUE) for e in root.findall(element_xpath) if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
        except IndexError:
            try:
                element = [e.get('value', DEFAULT_VALUE) for e in root.findall(element_xpath) if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_INITIAL][0]
            except IndexError:
                element = DEFAULT_VALUE
    else:
        element = None
        valid_meta = False
    return (element, valid_meta)


def extract_meta_without_fallback_helper(root, element_xpath):
    valid_meta = True
    if (root.find("./Test").get(element_xpath)) is not None:
        element = root.find("./Test").get(element_xpath, DEFAULT_VALUE)
    else:
        element = None
        valid_meta = False
    return (element, valid_meta)

