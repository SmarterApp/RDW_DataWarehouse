import logging
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper,\
    get_all_elements
from smarter_score_batcher.mapping.item_level import ItemLevelCsvColumns

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


def get_item_level_data(root):
    '''
    Generate and return item level data as list of lists for given xml root
    :param root: xml root document
    :returns: csv rows
    '''
    student_guid = extract_meta_with_fallback_helper(root, "./Examinee/ExamineeAttribute/[@name='StudentIdentifier']", "value", "context")
    matrix = []
    list_of_elements = get_all_elements(root, './Opportunity/Item')
    attribute_name_keys = ItemLevelCsvColumns.get_item_level_csv_keys(ItemLevelCsvColumns)
    for element_item in list_of_elements:
        row = [element_item.get(key) for key in attribute_name_keys]
        row.insert(1, student_guid)
        matrix.append(row)
    return matrix
