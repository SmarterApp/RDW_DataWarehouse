'''
Created on Aug 11, 2014

@author: dip
'''
from smarter_score_batcher.processing.assessment import XMLMeta, Mapping, DateMeta, IntegerMeta
from zope import component
from smarter_score_batcher.templates.asmt_template_manager import IMetadataTemplateManager,\
    get_template_key


class JSONHeaders:
    '''
    Data Structure used to store json landing zone file
    '''

    def __init__(self, template):
        self.values = template

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
        value = value
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
    opportunity = root.find("./Opportunity")
    test_node = root.find("./Test")
    subject = XMLMeta(test_node, ".", "subject")
    grade = IntegerMeta(test_node, ".", "grade")
    asmt_type = XMLMeta(test_node, ".", "assessmentType")
    year = XMLMeta(test_node, ".", "academicYear")

    meta_template_manager = component.queryUtility(IMetadataTemplateManager)
    meta_template = meta_template_manager.get_template(get_template_key(year.get_value(), asmt_type.get_value(), grade.get_value(), subject.get_value()))

    json_output = JSONHeaders(meta_template)

    mappings = [JSONMapping(XMLMeta(test_node, ".", "testId"), json_output, 'asmt_guid'),
                JSONMapping(DateMeta(opportunity, ".", "effectiveDate"), json_output, 'effective_date'),
                JSONMapping(subject, json_output, 'subject'),
                JSONMapping(asmt_type, json_output, 'asmt_type'),
                JSONMapping(XMLMeta(test_node, ".", "assessmentVersion"), json_output, 'asmt_version'),
                JSONMapping(year, json_output, 'asmt_year')]
    for m in mappings:
        m.evaluate()
    return json_output.get_values()
