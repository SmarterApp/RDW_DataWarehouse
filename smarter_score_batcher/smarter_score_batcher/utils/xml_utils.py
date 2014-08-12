import os
import logging
import csv

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")

DEFAULT_VALUE = 'NA'
ATTRIBUTE_CONTEXT_VALUE_FINAL = 'FINAL'
ATTRIBUTE_CONTEXT_VALUE_INITIAL = 'INITIAL'


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
