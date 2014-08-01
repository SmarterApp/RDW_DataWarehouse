import os
from pyramid.threadlocal import get_current_registry
from smarter_score_batcher.tasks.remote_file_writer import remote_write
from edapi.httpexceptions import EdApiHTTPPreconditionFailed


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

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
    try:
        tree = ET.parse(raw_xml_string)
        root = tree.getroot()
        m = extract_meta_names(root)
        if(m.valid_meta):
            file_path = create_path(ROOT_DIR, m)
            args = (file_path, raw_xml_string)
            settings = get_current_registry().settings
            timeout = settings.get("smarter_score_batcher.celery_timeout", 30)
            queue_name = settings.get('smarter_score_batcher.sync_queue')
            celery_response = remote_write.apply_async(args=args, queue=queue_name)
            # wait until file successfully written to disk
            return celery_response.get(timeout=timeout)
    except ET.ParseError:
        None
    return False


def validate_xml(raw_xml_string):
    if not raw_xml_string:
        raise EdApiHTTPPreconditionFailed("content cannot be empty")
    return True


def create_path(root_dir, meta):
    path = os.path.join(root_dir, meta.state_name, meta.academic_year, meta.asmt_type, meta.effective_date, meta.subject, meta.grade, meta.district_id)
    try:
        os.makedirs(path, exist_ok=True)
    except OSError:        
        return False
    return path


def extract_meta_names(root):
    '''Validates and extracts meta from the XML.
    
    Returns:
    True if meta for file path is valid. And the parts for folder creation.
    '''
    validMeta = True
    student_id = state_name = district_id = academic_year = asmt_type = subject = grade = effective_date = None
    
    if (root.find("./Examinee/ExamineeRelationship/[@name='StateName']")) is not None:
        try:
            state_name = [e.get('value', DEFAULT_VALUE) for e in root.findall("./Examinee/ExamineeRelationship/[@name='StateName']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
        except IndexError:
            try:
                state_name = [e.get('value', DEFAULT_VALUE) for e in root.findall("./Examinee/ExamineeRelationship/[@name='StateName']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_INITIAL][0]
            except IndexError:
                state_name = DEFAULT_VALUE
    else:
        validMeta = False 
   
    if (root.find("./Examinee/ExamineeRelationship/[@name='DistrictID']")) is not None:
        try:
            district_id = [e.get('value', DEFAULT_VALUE) for e in root.findall("./Examinee/ExamineeRelationship/[@name='DistrictID']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
        except IndexError:
            try:
                district_id = [e.get('value', DEFAULT_VALUE) for e in root.findall("./Examinee/ExamineeRelationship/[@name='DistrictID']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_INITIAL][0]
            except IndexError:
                district_id = DEFAULT_VALUE
    else:
        validMeta = False  
    
    if (root.find("./Examinee/ExamineeAttribute/[@name='SSID']")) is not None:
        try:
            student_id = [e.get('value', DEFAULT_VALUE) for e in root.findall("./Examinee/ExamineeAttribute/[@name='SSID']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
        except IndexError:
            try:
                student_id = [e.get('value', DEFAULT_VALUE) for e in root.findall("./Examinee/ExamineeAttribute/[@name='SSID']") if e.attrib['context'] == ATTRIBUTE_CONTEXT_VALUE_INITIAL][0]
            except IndexError:
                student_id = DEFAULT_VALUE
    else:
        validMeta = False
    if (root.find("./Test").get('assessmentType')) is not None:
        asmt_type = root.find("./Test").get('assessmentType', DEFAULT_VALUE)
    else:
        validMeta = False
    if (root.find("./Test").get('subject')) is not None:
        subject = root.find("./Test").get('subject', DEFAULT_VALUE)
    else:
        validMeta = False
    if (root.find("./Test").get('academicYear')) is not None:
        academic_year = root.find("./Test").get('academicYear', DEFAULT_VALUE)
    else:
        validMeta = False
    if (root.find("./Test").get('grade')) is not None:
        grade = root.find("./Test").get('grade', DEFAULT_VALUE)
    else:
        validMeta = False
    effective_date = 'NA'  # root.find("./test").get('effectiveDate', DEFAULT_VALUE)
    return Meta(validMeta, student_id, state_name, district_id, academic_year, asmt_type, subject, grade, effective_date)
