import os
import logging
import csv
from pyramid.threadlocal import get_current_registry
from smarter_score_batcher.tasks.remote_file_writer import remote_write
from smarter_score_batcher.tasks.remote_csv_writer import remote_csv_write
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


class TsbCsv:
    def __init__(self, key, student_guid, segmentId, position, clientId, operational, isSelected, format_type, score, scoreStatus, adminDate, numberVisits, strand, contentLevel, pageNumber, pageVisits, pageTime, dropped):
        self.__key = key
        self.__student_guid = student_guid
        self.__segmentId = segmentId
        self.__position = position
        self.__clientId = clientId
        self.__operational = operational
        self.__isSelected = isSelected
        self.__format_type = format_type
        self.__score = score
        self.__scoreStatus = scoreStatus
        self.__adminDate = adminDate
        self.__numberVisits = numberVisits
        self.__strand = strand
        self.__contentLevel = contentLevel
        self.__pageNumber = pageNumber
        self.__pageVisits = pageVisits
        self.__pageTime = pageTime
        self.__dropped = dropped

    @property
    def key(self):
        return self.__key

    @property
    def student_guid(self):
        return self.__student_guid

    @property
    def segmentId(self):
        return self.__segmentId

    @property
    def position(self):
        return self.__position

    @property
    def clientId(self):
        return self.__clientId

    @property
    def operational(self):
        return self.__operational

    @property
    def isSelected(self):
        return self.__isSelected

    @property
    def format_type(self):
        return self.__format_type

    @property
    def score(self):
        return self.__score

    @property
    def scoreStatus(self):
        return self.__scoreStatus

    @property
    def adminDate(self):
        return self.__adminDate

    @property
    def numberVisits(self):
        return self.__numberVisits

    @property
    def strand(self):
        return self.__strand

    @property
    def contentLevel(self):
        return self.__contentLevel

    @property
    def pageNumber(self):
        return self.__pageNumber

    @property
    def pageVisits(self):
        return self.__pageVisits

    @property
    def pageTime(self):
        return self.__pageTime

    @property
    def dropped(self):
        return self.__dropped


def process_xml(raw_xml_string):
    ''' Process tdsreport doc
    '''
    meta_names = extract_meta_names(raw_xml_string)
    if not meta_names.valid_meta:
        raise EdApiHTTPPreconditionFailed("Invalid XML")
    settings = get_current_registry().settings
    root_dir = settings.get("smarter_score_batcher.base_dir")
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
    root_dir = settings.get("smarter_score_batcher.base_dir")
    #Save csv to same folder as xml
    xml_file_path = create_path(root_dir, meta_names, generate_path_to_raw_xml)
    csv_file_path = create_path(root_dir, meta_names, generate_path_to_item_csv)
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        logger.error(str(e))
    matrix_to_feed_csv = get_all_elements_for_tsb_csv(root, './Opportunity/Item')
    queue_name = settings.get('smarter_score_batcher.sync_queue')
    args = (csv_file_path, matrix_to_feed_csv)
    celery_response = remote_csv_write.apply_async(args=args, queue=queue_name)
    return celery_response


#Returns a list of dictionaires of element attributes for all the times the element appears
def get_all_elements(root, xpath_of_element):
    list_of_dict = []
    for element_item in root.findall(xpath_of_element):
        attribute_dict = dict(element_item.items())
        list_of_dict.append(attribute_dict)
    return list_of_dict


def get_all_elements_for_tsb_csv(root, element_to_get):
    student_guid = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='SSID']", "value", "context")
    matrix = []
    list_of_elements = get_all_elements(root, element_to_get)
    for element_item in list_of_elements:
        key = element_item.get('key')
        segmentId = element_item.get('segmentId')
        position = element_item.get('position')
        clientId = element_item.get('clientId')
        operational = element_item.get('operational')
        isSelected = element_item.get('isSelected')
        format_type = element_item.get('format')
        score = element_item.get('score')
        scoreStatus = element_item.get('scoreStatus')
        adminDate = element_item.get('adminDate')
        numberVisits = element_item.get('numberVisits')
        strand = element_item.get('strand')
        contentLevel = element_item.get('contentLevel')
        pageNumber = element_item.get('pageNumber')
        pageVisits = element_item.get('pageVisits')
        pageTime = element_item.get('pageTime')
        dropped = element_item.get('dropped')
        columns = TsbCsv(key, student_guid, segmentId, position, clientId, operational, isSelected, format_type, score, scoreStatus, adminDate, numberVisits, strand, contentLevel, pageNumber, pageVisits, pageTime, dropped)
        row = [columns.key, columns.student_guid, columns.segmentId, columns.position, columns.clientId, columns.operational, columns.isSelected, columns.format_type, columns.score, columns.scoreStatus, columns.adminDate, columns.numberVisits, columns.strand, columns.contentLevel, columns.pageNumber, columns.pageVisits, columns.pageTime, columns.dropped]
        matrix.append(row)
    return matrix


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
