import logging
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper
from smarter_score_batcher.utils.xml_utils import extract_meta_without_fallback_helper
from edapi.httpexceptions import EdApiHTTPPreconditionFailed

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
    return generate_path(root_dir, **kwargs)


def extract_meta_names(raw_xml_string):
    '''Validates and extracts meta from the XML.
    Returns: True if meta for file path is valid. And the parts for folder creation.
    '''
    try:
        root = ET.fromstring(raw_xml_string)
        state_code = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeRelationship/[@name='StateName']", "value", "context")
        student_id = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='StudentIdentifier']", "value", "context")
        district_id = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeRelationship/[@name='DistrictID']", "value", "context")
        academic_year = extract_meta_without_fallback_helper(root, "./Test", "academicYear")
        asmt_type = extract_meta_without_fallback_helper(root, "./Test", "assessmentType")
        subject = extract_meta_without_fallback_helper(root, "./Test", "subject")
        grade = extract_meta_without_fallback_helper(root, "./Test", "grade")
        # TODO: This needs to be fixed
        effective_date = 'NA'  # root.find("./test").get('effectiveDate', DEFAULT_VALUE)
        validMeta = True if (state_code and student_id and district_id and academic_year and asmt_type and subject and grade) else False
        return Meta(validMeta, student_id, state_code, district_id, academic_year, asmt_type, subject, grade, effective_date)
    except ET.ParseError:
        raise EdApiHTTPPreconditionFailed("Invalid XML")
