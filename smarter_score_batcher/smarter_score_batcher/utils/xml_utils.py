import logging


logger = logging.getLogger("smarter_score_batcher")

DEFAULT_VALUE = 'NA'
ATTRIBUTE_CONTEXT_VALUE_FINAL = 'FINAL'
ATTRIBUTE_CONTEXT_VALUE_INITIAL = 'INITIAL'


def get_all_elements(root, xpath_of_element):
    '''
    Returns a list of dictionaires of element attributes for all the times the element appears
    '''
    list_of_dict = []
    for element_item in root.findall(xpath_of_element):
        attribute_dict = dict(element_item.items())
        list_of_dict.append(attribute_dict)
    return list_of_dict


def extract_meta_with_fallback_helper(root, element_xpath, attribute_to_get, attribute_to_compare):
    element = None
    if (root.find(element_xpath)) is not None:
        try:
            element = [e.get(attribute_to_get, DEFAULT_VALUE) for e in root.findall(element_xpath) if e.attrib[attribute_to_compare] == ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
        except IndexError:
            try:
                element = [e.get(attribute_to_get, DEFAULT_VALUE) for e in root.findall(element_xpath) if e.attrib[attribute_to_compare] == ATTRIBUTE_CONTEXT_VALUE_INITIAL][0]
            except IndexError:
                element = DEFAULT_VALUE
    return element


def extract_meta_without_fallback_helper(root, element_xpath, attribute_to_get):
    element = None
    if (root.find(element_xpath)) is not None:
        if(root.find(element_xpath).get(attribute_to_get)) is not None:
            element = root.find(element_xpath).get(attribute_to_get, DEFAULT_VALUE)
    return element
