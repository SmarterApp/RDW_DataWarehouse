'''
Created on Oct 2, 2014

@author: tosako
'''
from smarter_score_batcher.utils.constants import PerformanceMetadataConstatns
from smarter_score_batcher.error.exceptions import MetadataException
from smarter_score_batcher.error.error_codes import ErrorSource
import logging
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


logger = logging.getLogger("smarter_score_batcher")


def generate_performance_metadata(xml_string):
    '''
    generating performance metadata by given xml file path
    '''
    try:
        performanceMedadata = PerformanceMetadata()
        root = ET.fromstring(xml_string)
        properties = list(root.iter('property'))
        for _property in properties:
            name = _property.attrib['name']
            value = _property.attrib['value']
            if name == 'subject':
                performanceMedadata.set_subject(value)
                break
        performancelevels = list(root.find('./reporting/performancelevels').iter('performancelevel'))
        min_value = None
        max_value = None
        for performancelevel in performancelevels:
            plevel = performancelevel.attrib['plevel']
            scaledlo = performancelevel.attrib['scaledlo']
            scaledhi = performancelevel.attrib['scaledhi']
            int_scaledlo = int(scaledlo) if type(scaledlo) is str else scaledlo
            int_scaledhi = int(scaledhi) if type(scaledhi) is str else scaledhi
            cutpoint = 'set_level' + plevel + '_cutPoint'
            getattr(performanceMedadata, cutpoint)(int_scaledlo)
            if min_value is None or min_value > int_scaledlo:
                min_value = int_scaledlo
            if max_value is None or max_value < int_scaledhi:
                max_value = int_scaledhi
        performanceMedadata.set_overall_minScore(min_value)
        performanceMedadata.set_overall_maxScore(max_value)
        return _format_performance_metadata(performanceMedadata)
    except Exception as e:
        logging.error('error while loading metadata from xml: ' + str(e))
        raise MetadataException('error while loading metadata from xml: ' + str(e), err_source=ErrorSource.GENERATE_PERFORMANCE_METADATA)


def _format_performance_metadata(performancelevel):
    '''
    compose performance metadata
    '''
    meta = {}
    meta[PerformanceMetadataConstatns.IDENTIFICATION] = {PerformanceMetadataConstatns.SUBJECT: performancelevel.get_subject()}
    meta[PerformanceMetadataConstatns.OVERALL] = {PerformanceMetadataConstatns.MINSCORE: str(performancelevel.get_overall_minScore()),
                                                  PerformanceMetadataConstatns.MAXSCORE: str(performancelevel.get_overall_maxScore())
                                                  }
    meta[PerformanceMetadataConstatns.PERFORMANCELEVELS] = {PerformanceMetadataConstatns.LEVEL1: {PerformanceMetadataConstatns.CUTPOINT: str(performancelevel.get_level1_cutPoint())},
                                                            PerformanceMetadataConstatns.LEVEL2: {PerformanceMetadataConstatns.CUTPOINT: str(performancelevel.get_level2_cutPoint())},
                                                            PerformanceMetadataConstatns.LEVEL3: {PerformanceMetadataConstatns.CUTPOINT: str(performancelevel.get_level3_cutPoint())},
                                                            PerformanceMetadataConstatns.LEVEL4: {PerformanceMetadataConstatns.CUTPOINT: str(performancelevel.get_level4_cutPoint())},
                                                            }
    meta[PerformanceMetadataConstatns.CLAIMS] = {PerformanceMetadataConstatns.CLAIM1: {PerformanceMetadataConstatns.MINSCORE: str(performancelevel.get_claim1_minScore()),
                                                                                       PerformanceMetadataConstatns.MAXSCORE: str(performancelevel.get_claim1_maxScore())},
                                                 PerformanceMetadataConstatns.CLAIM2: {PerformanceMetadataConstatns.MINSCORE: str(performancelevel.get_claim2_minScore()),
                                                                                       PerformanceMetadataConstatns.MAXSCORE: str(performancelevel.get_claim2_maxScore())},
                                                 PerformanceMetadataConstatns.CLAIM3: {PerformanceMetadataConstatns.MINSCORE: str(performancelevel.get_claim3_minScore()),
                                                                                       PerformanceMetadataConstatns.MAXSCORE: str(performancelevel.get_claim3_maxScore())},
                                                 PerformanceMetadataConstatns.CLAIM4: {PerformanceMetadataConstatns.MINSCORE: str(performancelevel.get_claim4_minScore()),
                                                                                       PerformanceMetadataConstatns.MAXSCORE: str(performancelevel.get_claim4_maxScore())}
                                                 }
    return meta


class PerformanceMetadata():
    '''
    Performance Metadata value holder class
    '''
    def __init__(self):
        self.__subject = None
        self.__overall_minScore = None
        self.__overall_maxScore = None
        self.__level1_cutPoint = 0
        self.__level2_cutPoint = 0
        self.__level3_cutPoint = 0
        self.__level4_cutPoint = 0

    def get_subject(self):
        return self.__subject

    def get_overall_minScore(self):
        return self.__overall_minScore

    def get_overall_maxScore(self):
        return self.__overall_maxScore

    def get_level1_cutPoint(self):
        return self.__level1_cutPoint

    def get_level2_cutPoint(self):
        return self.__level2_cutPoint

    def get_level3_cutPoint(self):
        return self.__level3_cutPoint

    def get_level4_cutPoint(self):
        return self.__level4_cutPoint

    def get_claim1_minScore(self):
        return 0

    def get_claim1_maxScore(self):
        return 0

    def get_claim2_minScore(self):
        return 0

    def get_claim2_maxScore(self):
        return 0

    def get_claim3_minScore(self):
        return 0

    def get_claim3_maxScore(self):
        return 0

    def get_claim4_minScore(self):
        return 0

    def get_claim4_maxScore(self):
        return 0

    def set_subject(self, value):
        self.__subject = value

    def set_overall_minScore(self, value):
        if self.__overall_minScore is None or self.__overall_minScore > value:
            self.__overall_minScore = value

    def set_overall_maxScore(self, value):
        if self.__overall_maxScore is None or self.__overall_maxScore < value:
            self.__overall_maxScore = value

    def set_level1_cutPoint(self, value):
        self.__level1_cutPoint = value

    def set_level2_cutPoint(self, value):
        self.__level2_cutPoint = value

    def set_level3_cutPoint(self, value):
        self.__level3_cutPoint = value

    def set_level4_cutPoint(self, value):
        self.__level4_cutPoint = value
