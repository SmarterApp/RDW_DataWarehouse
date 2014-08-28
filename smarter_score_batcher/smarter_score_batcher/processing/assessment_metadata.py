'''
Created on Aug 11, 2014

@author: dip
'''
from copy import deepcopy
from smarter_score_batcher.processing.assessment import XMLMeta, Mapping


class JSONHeaders:
    '''
    Data Structure used to store json landing zone file
    '''
    lz_json = {"Content": "assessment",
               "Identification": {"Guid": None,
                                  "Type": None,
                                  "Year": None,
                                  "Period": None,
                                  "Version": None,
                                  "Subject": None,
                                  "EffectiveDate": None
                                  },
               "Overall": {"MinScore": None,
                           "MaxScore": None},
               "PerformanceLevels": {"Level1": {"Name": None},
                                     "Level2": {"Name": None,
                                                "Cutpoint": None},
                                     "Level3": {"Name": None,
                                                "Cutpoint": None},
                                     "Level4": {"Name": None,
                                                "Cutpoint": None},
                                     "Level5": {"Name": None,
                                                "Cutpoint": None}},
               "Claims": {"Claim1": {"Name": None,
                                     "MinScore": None,
                                     "MaxScore": None},
                          "Claim2": {"Name": None,
                                     "MinScore": None,
                                     "MaxScore": None},
                          "Claim3": {"Name": None,
                                     "MinScore": None,
                                     "MaxScore": None},
                          "Claim4": {"Name": None,
                                     "MinScore": None,
                                     "MaxScore": None}},
               "ClaimPerformanceLevels": {"Level1": {"Name": None},
                                          "Level2": {"Name": None},
                                          "Level3": {"Name": None}}
               }

    def __init__(self):
        self.values = deepcopy(JSONHeaders.lz_json)

    def get_values(self):
        return self.values

    @property
    def asmt_guid(self):
        return self.values['Identification']['Guid']

    @asmt_guid.setter
    def asmt_guid(self, value):
        self.values['Identification']['Guid'] = value

    @property
    def asmt_type(self):
        return self.values['Identification']['Type']

    @asmt_type.setter
    def asmt_type(self, value):
        self.values['Identification']['Type'] = value

    @property
    def asmt_year(self):
        return self.values['Identification']['Year']

    @asmt_year.setter
    def asmt_year(self, value):
        self.values['Identification']['Year'] = value

    @property
    def asmt_period(self):
        return self.values['Identification']['Period']

    @asmt_period.setter
    def asmt_period(self, value):
        self.values['Identification']['Period'] = value

    @property
    def asmt_version(self):
        return self.values['Identification']['Version']

    @asmt_version.setter
    def asmt_version(self, value):
        self.values['Identification']['Version'] = value

    @property
    def subject(self):
        return self.values['Identification']['Subject']

    @subject.setter
    def subject(self, value):
        self.values['Identification']['Subject'] = value

    @property
    def effective_date(self):
        return self.values['Identification']['EffectiveDate']

    @effective_date.setter
    def effective_date(self, value):
        self.values['Identification']['EffectiveDate'] = value

    @property
    def min_score(self):
        return self.values['Overall']['MinScore']

    @min_score.setter
    def min_score(self, value):
        self.values['Overall']['MinScore'] = value

    @property
    def max_score(self):
        return self.values['Overall']['MaxScore']

    @max_score.setter
    def max_score(self, value):
        self.values['Overall']['MaxScore'] = value

    @property
    def level1_name(self):
        return self.values['PerformanceLevels']['Level1']['Name']

    @level1_name.setter
    def level1_name(self, value):
        self.values['PerformanceLevels']['Level1']['Name'] = value

    @property
    def level2_name(self):
        return self.values['PerformanceLevels']['Level2']['Name']

    @level2_name.setter
    def level2_name(self, value):
        self.values['PerformanceLevels']['Level2']['Name'] = value

    @property
    def level3_name(self):
        return self.values['PerformanceLevels']['Level3']['Name']

    @level3_name.setter
    def level3_name(self, value):
        self.values['PerformanceLevels']['Level3']['Name'] = value

    @property
    def level4_name(self):
        return self.values['PerformanceLevels']['Level4']['Name']

    @level4_name.setter
    def level4_name(self, value):
        self.values['PerformanceLevels']['Level4']['Name'] = value

    @property
    def level5_name(self):
        return self.values['PerformanceLevels']['Level5']['Name']

    @level5_name.setter
    def level5_name(self, value):
        self.values['PerformanceLevels']['Level5']['Name'] = value

    @property
    def level2_cutpoint(self):
        return self.values['PerformanceLevels']['Level2']['Cutpoint']

    @level2_cutpoint.setter
    def level2_cutpoint(self, value):
        self.values['PerformanceLevels']['Level2']['Cutpoint'] = value

    @property
    def level3_cutpoint(self):
        return self.values['PerformanceLevels']['Level3']['Cutpoint']

    @level3_cutpoint.setter
    def level3_cutpoint(self, value):
        self.values['PerformanceLevels']['Level3']['Cutpoint'] = value

    @property
    def level4_cutpoint(self):
        return self.values['PerformanceLevels']['Level4']['Cutpoint']

    @level4_cutpoint.setter
    def level4_cutpoint(self, value):
        self.values['PerformanceLevels']['Level4']['Cutpoint'] = value

    @property
    def level5_cutpoint(self):
        return self.values['PerformanceLevels']['Level5']['Cutpoint']

    @level5_cutpoint.setter
    def level5_cutpoint(self, value):
        self.values['PerformanceLevels']['Level5']['Cutpoint'] = value

    @property
    def claim1_name(self):
        return self.values['Claims']['Claim1']['Name']

    @claim1_name.setter
    def claim1_name(self, value):
        self.values['Claims']['Claim1']['Name'] = value

    @property
    def claim1_min_score(self):
        return self.values['Claims']['Claim1']['MinScore']

    @claim1_min_score.setter
    def claim1_min_score(self, value):
        self.values['Claims']['Claim1']['MinScore'] = value

    @property
    def claim1_max_score(self):
        return self.values['Claims']['Claim1']['MaxScore']

    @claim1_max_score.setter
    def claim1_max_score(self, value):
        self.values['Claims']['Claim1']['MaxScore'] = value

    @property
    def claim2_name(self):
        return self.values['Claims']['Claim2']['Name']

    @claim2_name.setter
    def claim2_name(self, value):
        self.values['Claims']['Claim2']['Name'] = value

    @property
    def claim2_min_score(self):
        return self.values['Claims']['Claim2']['MinScore']

    @claim2_min_score.setter
    def claim2_min_score(self, value):
        self.values['Claims']['Claim2']['MinScore'] = value

    @property
    def claim2_max_score(self):
        return self.values['Claims']['Claim2']['MaxScore']

    @claim2_max_score.setter
    def claim2_max_score(self, value):
        self.values['Claims']['Claim2']['MaxScore'] = value

    @property
    def claim3_name(self):
        return self.values['Claims']['Claim3']['Name']

    @claim3_name.setter
    def claim3_name(self, value):
        self.values['Claims']['Claim3']['Name'] = value

    @property
    def claim3_min_score(self):
        return self.values['Claims']['Claim3']['MinScore']

    @claim3_min_score.setter
    def claim3_min_score(self, value):
        self.values['Claims']['Claim3']['MinScore'] = value

    @property
    def claim3_max_score(self):
        return self.values['Claims']['Claim3']['MaxScore']

    @claim3_max_score.setter
    def claim3_max_score(self, value):
        self.values['Claims']['Claim3']['MaxScore'] = value

    @property
    def claim4_name(self):
        return self.values['Claims']['Claim4']['Name']

    @claim4_name.setter
    def claim4_name(self, value):
        self.values['Claims']['Claim4']['Name'] = value

    @property
    def claim4_min_score(self):
        return self.values['Claims']['Claim4']['MinScore']

    @claim4_min_score.setter
    def claim4_min_score(self, value):
        self.values['Claims']['Claim4']['MinScore'] = value

    @property
    def claim4_max_score(self):
        return self.values['Claims']['Claim4']['MaxScore']

    @claim4_max_score.setter
    def claim4_max_score(self, value):
        self.values['Claims']['Claim4']['MaxScore'] = value

    @property
    def claim_perf_level1_name(self):
        return self.values['ClaimPerformanceLevels']['Level1']['Name']

    @claim_perf_level1_name.setter
    def claim_perf_level1_name(self, value):
        self.values['ClaimPerformanceLevels']['Level1']['Name'] = value

    @property
    def claim_perf_level2_name(self):
        return self.values['ClaimPerformanceLevels']['Level2']['Name']

    @claim_perf_level2_name.setter
    def claim_perf_level2_name(self, value):
        self.values['ClaimPerformanceLevels']['Level2']['Name'] = value

    @property
    def claim_perf_level3_name(self):
        return self.values['ClaimPerformanceLevels']['Level3']['Name']

    @claim_perf_level3_name.setter
    def claim_perf_level3_name(self, value):
        self.values['ClaimPerformanceLevels']['Level3']['Name'] = value


class JSONMapping(Mapping):
    '''
    Data Structure used to store mapping values from xml to csv
    '''
    def __init__(self, src, target, property_name):
        super(JSONMapping, self).__init__(src, target)
        self.property = property_name

    def evaluate(self):
        setattr(self.target, self.property, self.src.get_value())


def get_assessment_metadata_mapping(root):
    '''
    Returns the json format needed for landing zone assessment file
    '''
    json_output = JSONHeaders()
    opportunity = root.find("./Opportunity")
    test_node = root.find("./Test")

    mappings = [JSONMapping(XMLMeta(test_node, ".", "testId"), json_output, 'asmt_guid'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='Text']", "value"), json_output, 'claim1_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='Text']", "value"), json_output, 'claim2_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='Text']", "value"), json_output, 'claim3_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='Text']", "value"), json_output, 'claim4_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='PerformanceLevel'][@measureLabel='Level1']", "value"), json_output, 'level1_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='PerformanceLevel'][@measureLabel='Level2']", "value"), json_output, 'level2_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='PerformanceLevel'][@measureLabel='Level3']", "value"), json_output, 'level3_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='PerformanceLevel'][@measureLabel='Level4']", "value"), json_output, 'level4_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='ClaimPerformanceLevel'][@measureLabel='Level1']", "value"), json_output, 'claim_perf_level1_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='ClaimPerformanceLevel'][@measureLabel='Level2']", "value"), json_output, 'claim_perf_level2_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='ClaimPerformanceLevel'][@measureLabel='Level3']", "value"), json_output, 'claim_perf_level3_name'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='MaxScore']", "value"), json_output, 'claim1_max_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='MinScore']", "value"), json_output, 'claim1_min_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='MaxScore']", "value"), json_output, 'claim2_max_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='MinScore']", "value"), json_output, 'claim2_min_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='MaxScore']", "value"), json_output, 'claim3_max_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='MinScore']", "value"), json_output, 'claim3_min_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='MaxScore']", "value"), json_output, 'claim4_max_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='MinScore']", "value"), json_output, 'claim4_min_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='CutPoint1']", "value"), json_output, 'level2_cutpoint'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='CutPoint2']", "value"), json_output, 'level3_cutpoint'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='CutPoint3']", "value"), json_output, 'level4_cutpoint'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='CutPoint4']", "value"), json_output, 'level5_cutpoint'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='MinScore']", "value"), json_output, 'min_score'),
                JSONMapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='MaxScore']", "value"), json_output, 'max_score'),
                JSONMapping(XMLMeta(opportunity, ".", "effectiveDate"), json_output, 'effective_date'),
                JSONMapping(XMLMeta(test_node, ".", "subject"), json_output, 'subject'),
                JSONMapping(XMLMeta(test_node, ".", "assessmentType"), json_output, 'asmt_type'),
                JSONMapping(XMLMeta(test_node, ".", "assessmentVersion"), json_output, 'asmt_version'),
                JSONMapping(XMLMeta(test_node, ".", "academicYear"), json_output, 'asmt_year')]
    for m in mappings:
        m.evaluate()
    return json_output.get_values()
