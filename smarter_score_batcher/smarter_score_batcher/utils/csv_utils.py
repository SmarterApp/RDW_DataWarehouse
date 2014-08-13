import logging
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper,\
    get_all_elements
from smarter_score_batcher.mapping.csv_metadata import get_csv_mapping
from smarter_score_batcher.mapping.json_metadata import get_json_mapping


logger = logging.getLogger("smarter_score_batcher")


def get_item_level_data(root):
    student_guid = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='StudentIdentifier']", "value", "context")
    matrix = []
    list_of_elements = get_all_elements(root, './Opportunity/Item')
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
        row = [key, student_guid, segmentId, position, clientId, operational, isSelected, format_type, score, scoreStatus, adminDate, numberVisits, strand, contentLevel, pageNumber, pageVisits, pageTime, dropped]
        matrix.append(row)
    return matrix


def process_assessment_data(root):
    # csv_data is a dictionary that can be inserted into db
    csv_data = get_csv_mapping(root)
    # json_data is a dictionary of the json file format
    json_data = get_json_mapping(root)
    # TODO: write to db in next story
