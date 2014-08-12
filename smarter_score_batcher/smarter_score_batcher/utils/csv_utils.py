import logging
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


#Returns a list of dictionaires of element attributes for all the times the element appears
def get_all_elements(root, xpath_of_element):
    list_of_dict = []
    for element_item in root.findall(xpath_of_element):
        attribute_dict = dict(element_item.items())
        list_of_dict.append(attribute_dict)
    return list_of_dict


def get_all_elements_for_tsb_csv(root, element_to_get):
    student_guid = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='StudentIdentifier']", "value", "context")
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
        row = [key, student_guid, segmentId, position, clientId, operational, isSelected, format_type, score, scoreStatus, adminDate, numberVisits, strand, contentLevel, pageNumber, pageVisits, pageTime, dropped]
        matrix.append(row)
    return matrix
