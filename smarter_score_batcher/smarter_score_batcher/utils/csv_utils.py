import os
import logging
import csv
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logger = logging.getLogger("smarter_score_batcher")


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
