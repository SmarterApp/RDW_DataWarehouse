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
        self.__student_id = student_id
        self.__state_name = state_name
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
    def state_name(self):
        return self.__state_name
        
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
    file_path = create_path(ROOT_DIR, meta_names)
    args = (file_path, raw_xml_string)
    settings = get_current_registry().settings
    timeout = settings.get("smarter_score_batcher.celery_timeout", 30)
    queue_name = settings.get('smarter_score_batcher.sync_queue')
    celery_response = remote_write.apply_async(args=args, queue=queue_name)
    # wait until file successfully written to disk
    return celery_response.get(timeout=timeout)


def create_path(root_dir, meta):
    path = os.path.join(root_dir, meta.student_id, meta.state_name, meta.district_id, meta.academic_year, meta.asmt_type, meta.subject, meta.grade, meta.effective_date)
    return path


def extract_meta_names(raw_xml_string):
    '''Validates and extracts meta from the XML.
    Returns: True if meta for file path is valid. And the parts for folder creation.
    '''
    try:
        root = ET.fromstring(raw_xml_string)
        state_name = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeRelationship/[@name='StateName']", "value", "context" )
        student_id = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='SSID']", "value", "context" )
        district_id = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeRelationship/[@name='DistrictID']", "value", "context" )
        academic_year = extract_meta_without_fallback_helper(root, "./Test", "academicYear")
        asmt_type = extract_meta_without_fallback_helper(root, "./Test", "assessmentType")
        subject = extract_meta_without_fallback_helper(root, "./Test", "subject")
        grade = extract_meta_without_fallback_helper(root, "./Test", "grade")
        effective_date = 'NA'  # root.find("./test").get('effectiveDate', DEFAULT_VALUE)
        validMeta = state_name and student_id and district_id and academic_year and asmt_type and subject and grade
        return Meta(validMeta, student_id, state_name, district_id, academic_year, asmt_type, subject, grade, effective_date)
    except ET.ParseError:
        raise EdApiHTTPPreconditionFailed("Invalid XML")
        

def extract_meta_with_fallback_helper(root, element_xpath, attribute_to_get, attribute_to_compare):
    if (root.find(element_xpath)) is not None:
        try:
            element = [e.get(attribute_to_get, DEFAULT_VALUE) for e in root.findall(element_xpath) if e.attrib[attribute_to_compare] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
        except IndexError:
            try:
                element = [e.get(attribute_to_get, DEFAULT_VALUE) for e in root.findall(element_xpath) if e.attrib[attribute_to_compare] == ATTRIBUTE_CONTEXT_VALUE_INITIAL][0]
            except IndexError:
                element = DEFAULT_VALUE
    else:
        element = False
    return element


def extract_meta_without_fallback_helper(root, element_xpath, attribute_to_get):
    element = False
    if (root.find(element_xpath)) is not None:
        if(root.find(element_xpath).get(attribute_to_get)) is not None:
            element = root.find(element_xpath).get(attribute_to_get, DEFAULT_VALUE)
    return element
