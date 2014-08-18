'''
Created on Aug 8, 2014

@author: dip
'''
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper,\
    extract_meta_without_fallback_helper


class XMLMeta:
    '''
    Used for storing and extracting elements from xml
    '''
    def __init__(self, root, xpath, attribute, attribute_to_compare=None):
        self.root = root
        self.path = xpath
        self.attribute = attribute
        self.attribute_to_compare = attribute_to_compare

    def get_value(self):
        if self.attribute_to_compare:
            val = extract_meta_with_fallback_helper(self.root, self.path, self.attribute, self.attribute_to_compare)
        else:
            val = extract_meta_without_fallback_helper(self.root, self.path, self.attribute)
        return val


class AccommodationMeta(XMLMeta):
    '''
    Accommodation Specific - Perhaps to handle default values
    '''
    def __init__(self, root, xpath, attribute, attribute_to_compare):
        super(AccommodationMeta, self).__init__(root, xpath, attribute, attribute_to_compare)

    def get_value(self):
        val = super(AccommodationMeta, self).get_value()
        # TODO:  Some defaults are different
        return '0' if val is None else val


class Mapping:
    '''
    Used for storing and evaluating mapping from xml to csv
    '''
    def __init__(self, src, target):
        self.src = src
        self.target = target

    def evaluate(self):
        return self.src.get_value()


class AssessmentHeaders:
    '''
    Constants for assessment csv landing zone file
    '''
    # In the order of csv headers
    StateAbbreviation = 'StateAbbreviation'
    ResponsibleDistrictIdentifier = 'ResponsibleDistrictIdentifier'
    OrganizationName = 'OrganizationName'
    ResponsibleSchoolIdentifier = 'ResponsibleSchoolIdentifier'
    NameOfInstitution = 'NameOfInstitution'
    StudentIdentifier = 'StudentIdentifier'
    ExternalSSID = 'ExternalSSID'
    FirstName = 'FirstName'
    MiddleName = 'MiddleName'
    LastOrSurname = 'LastOrSurname'
    Sex = 'Sex'
    Birthdate = 'Birthdate'
    GradeLevelWhenAssessed = 'GradeLevelWhenAssessed'
    HispanicOrLatinoEthnicity = 'HispanicOrLatinoEthnicity'
    AmericanIndianOrAlaskaNative = 'AmericanIndianOrAlaskaNative'
    Asian = 'Asian'
    BlackOrAfricanAmerican = 'BlackOrAfricanAmerican'
    NativeHawaiianOrOtherPacificIslander = 'NativeHawaiianOrOtherPacificIslander'
    White = 'White'
    DemographicRaceTwoOrMoreRaces = 'DemographicRaceTwoOrMoreRaces'
    IDEAIndicator = 'IDEAIndicator'
    LEPStatus = 'LEPStatus'
    Section504Status = 'Section504Status'
    EconomicDisadvantageStatus = 'EconomicDisadvantageStatus'
    MigrantStatus = 'MigrantStatus'
    Group1Id = 'Group1Id'
    Group1Text = 'Group1Text'
    Group2Id = 'Group2Id'
    Group2Text = 'Group2Text'
    AssessmentGuid = 'AssessmentGuid'
    AssessmentSessionLocationId = 'AssessmentSessionLocationId'
    AssessmentSessionLocation = 'AssessmentSessionLocation'
    AssessmentAdministrationFinishDate = 'AssessmentAdministrationFinishDate'
    AssessmentYear = 'AssessmentYear'
    AssessmentType = 'AssessmentType'
    AssessmentAcademicSubject = 'AssessmentAcademicSubject'
    AssessmentLevelForWhichDesigned = 'AssessmentLevelForWhichDesigned'
    AssessmentSubtestResultScoreValue = 'AssessmentSubtestResultScoreValue'
    AssessmentSubtestMinimumValue = 'AssessmentSubtestMinimumValue'
    AssessmentSubtestMaximumValue = 'AssessmentSubtestMaximumValue'
    AssessmentPerformanceLevelIdentifier = 'AssessmentPerformanceLevelIdentifier'
    AssessmentSubtestResultScoreClaim1Value = 'AssessmentSubtestResultScoreClaim1Value'
    AssessmentSubtestClaim1MinimumValue = 'AssessmentSubtestClaim1MinimumValue'
    AssessmentSubtestClaim1MaximumValue = 'AssessmentSubtestClaim1MaximumValue'
    AssessmentClaim1PerformanceLevelIdentifier = 'AssessmentClaim1PerformanceLevelIdentifier'
    AssessmentSubtestResultScoreClaim2Value = 'AssessmentSubtestResultScoreClaim2Value'
    AssessmentSubtestClaim2MinimumValue = 'AssessmentSubtestClaim2MinimumValue'
    AssessmentSubtestClaim2MaximumValue = 'AssessmentSubtestClaim2MaximumValue'
    AssessmentClaim2PerformanceLevelIdentifier = 'AssessmentClaim2PerformanceLevelIdentifier'
    AssessmentSubtestResultScoreClaim3Value = 'AssessmentSubtestResultScoreClaim3Value'
    AssessmentSubtestClaim3MinimumValue = 'AssessmentSubtestClaim3MinimumValue'
    AssessmentSubtestClaim3MaximumValue = 'AssessmentSubtestClaim3MaximumValue'
    AssessmentClaim3PerformanceLevelIdentifier = 'AssessmentClaim3PerformanceLevelIdentifier'
    AssessmentSubtestResultScoreClaim4Value = 'AssessmentSubtestResultScoreClaim4Value'
    AssessmentSubtestClaim4MinimumValue = 'AssessmentSubtestClaim4MinimumValue'
    AssessmentSubtestClaim4MaximumValue = 'AssessmentSubtestClaim4MaximumValue'
    AssessmentClaim4PerformanceLevelIdentifier = 'AssessmentClaim4PerformanceLevelIdentifier'
    AccommodationAmericanSignLanguage = 'AccommodationAmericanSignLanguage'
    AccommodationSignLanguageHumanIntervention = 'AccommodationSignLanguageHumanIntervention'
    AccommodationBraille = 'AccommodationBraille'
    AccommodationClosedCaptioning = 'AccommodationClosedCaptioning'
    AccommodationTextToSpeech = 'AccommodationTextToSpeech'
    AccommodationAbacus = 'AccommodationAbacus'
    AccommodationAlternateResponseOptions = 'AccommodationAlternateResponseOptions'
    AccommodationCalculator = 'AccommodationCalculator'
    AccommodationMultiplicationTable = 'AccommodationMultiplicationTable'
    AccommodationPrintOnDemand = 'AccommodationPrintOnDemand'
    AccommodationReadAloud = 'AccommodationReadAloud'
    AccommodationScribe = 'AccommodationScribe'
    AccommodationSpeechToText = 'AccommodationSpeechToText'
    AccommodationStreamlineMode = 'AccommodationStreamlineMode'


class AssessmentData:
    def __init__(self, mappings):
        self.__mappings = mappings
        self.__header = []
        self.__values = []

    def add(self, header, value):
        self.__header.append(header)
        self.__values.append(value)

    @property
    def header(self):
        return self.__header

    @property
    def values(self):
        return self.__values

    def evaluate(self):
        for m in self.__mappings:
            # Save the CSV Header, and Value Extracted from XML
            self.add(m.target, m.evaluate())


def get_assessment_mapping(root):
    '''
    Returns the landing zone format of assessment csv file
    '''
    examinee = root.find("./Examinee")
    opportunity = root.find("./Opportunity")
    test_node = root.find("./Test")

    # In the order of the LZ mapping for easier maintenance
    mappings = AssessmentData([Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='StateName']", "value", "context"), AssessmentHeaders.StateAbbreviation),
                               Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='DistrictID']", "value", "context"), AssessmentHeaders.ResponsibleSchoolIdentifier),
                               Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='DistrictName']", "value", "context"), AssessmentHeaders.OrganizationName),
                               Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='SchoolID']", "value", "context"), AssessmentHeaders.ResponsibleSchoolIdentifier),
                               Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='SchoolName']", "value", "context"), AssessmentHeaders.NameOfInstitution),

                               Mapping(XMLMeta(examinee, ".", "key"), AssessmentHeaders.StudentIdentifier),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='AlternateSSID']", "value", "context"), AssessmentHeaders.ExternalSSID),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='FirstName']", "value", "context"), AssessmentHeaders.FirstName),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='MiddleName']", "value", "context"), AssessmentHeaders.MiddleName),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='LastOrSurname']", "value", "context"), AssessmentHeaders.LastOrSurname),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Sex']", "value", "context"), AssessmentHeaders.Sex),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Birthdate']", "value", "context"), AssessmentHeaders.Birthdate),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='GradeLevelWhenAssessed']", "value", "context"), AssessmentHeaders.GradeLevelWhenAssessed),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='HispanicOrLatinoEthnicity']", "value", "context"), AssessmentHeaders.HispanicOrLatinoEthnicity),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='AmericanIndianOrAlaskaNative']", "value", "context"), AssessmentHeaders.AmericanIndianOrAlaskaNative),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Asian']", "value", "context"), AssessmentHeaders.Asian),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='BlackOrAfricanAmerican']", "value", "context"), AssessmentHeaders.BlackOrAfricanAmerican),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='NativeHawaiianOrOtherPacificIslander']", "value", "context"), AssessmentHeaders.NativeHawaiianOrOtherPacificIslander),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='White']", "value", "context"), AssessmentHeaders.White),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='DemographicRaceTwoOrMoreRaces']", "value", "context"), AssessmentHeaders.DemographicRaceTwoOrMoreRaces),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='IDEAIndicator']", "value", "context"), AssessmentHeaders.IDEAIndicator),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='LEPStatus']", "value", "context"), AssessmentHeaders.LEPStatus),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Section504Status']", "value", "context"), AssessmentHeaders.Section504Status),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='EconomicDisadvantageStatus']", "value", "context"), AssessmentHeaders.EconomicDisadvantageStatus),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='MigrantStatus']", "value", "context"), AssessmentHeaders.MigrantStatus),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Group1Id']", "value", "context"), AssessmentHeaders.Group1Id),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Group1Text']", "value", "context"), AssessmentHeaders.Group1Text),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Group2Id']", "value", "context"), AssessmentHeaders.Group2Id),
                               Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Group2Text']", "value", "context"), AssessmentHeaders.Group2Text),

                               Mapping(XMLMeta(test_node, ".", "testId"), AssessmentHeaders.AssessmentGuid),
                               Mapping(XMLMeta(opportunity, ".", "oppId"), AssessmentHeaders.AssessmentSessionLocationId),
                               Mapping(XMLMeta(opportunity, ".", "server"), AssessmentHeaders.AssessmentSessionLocation),
                               Mapping(XMLMeta(opportunity, ".", "dateCompleted"), AssessmentHeaders.AssessmentAdministrationFinishDate),
                               Mapping(XMLMeta(test_node, ".", "academicYear"), AssessmentHeaders.AssessmentYear),
                               Mapping(XMLMeta(test_node, ".", "assessmentType"), AssessmentHeaders.AssessmentType),
                               Mapping(XMLMeta(test_node, ".", "subject"), AssessmentHeaders.AssessmentAcademicSubject),
                               Mapping(XMLMeta(test_node, ".", "grade"), AssessmentHeaders.AssessmentLevelForWhichDesigned),

                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='ScaleScore']", "value"), AssessmentHeaders.AssessmentSubtestResultScoreValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='MinScore']", "value"), AssessmentHeaders.AssessmentSubtestMinimumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='MaxScore']", "value"), AssessmentHeaders.AssessmentSubtestMaximumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='PerformanceLevel']", "value"), AssessmentHeaders.AssessmentPerformanceLevelIdentifier),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='ScaleScore']", "value"), AssessmentHeaders.AssessmentSubtestResultScoreClaim1Value),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='MinScore']", "value"), AssessmentHeaders.AssessmentSubtestClaim1MinimumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='MaxScore']", "value"), AssessmentHeaders.AssessmentSubtestClaim1MaximumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='PerformanceLevel']", "value"), AssessmentHeaders.AssessmentClaim1PerformanceLevelIdentifier),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='ScaleScore']", "value"), AssessmentHeaders.AssessmentSubtestResultScoreClaim2Value),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='MinScore']", "value"), AssessmentHeaders.AssessmentSubtestClaim2MinimumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='MaxScore']", "value"), AssessmentHeaders.AssessmentSubtestClaim2MaximumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='PerformanceLevel']", "value"), AssessmentHeaders.AssessmentClaim2PerformanceLevelIdentifier),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='ScaleScore']", "value"), AssessmentHeaders.AssessmentSubtestResultScoreClaim3Value),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='MinScore']", "value"), AssessmentHeaders.AssessmentSubtestClaim3MinimumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='MaxScore']", "value"), AssessmentHeaders.AssessmentSubtestClaim3MaximumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='PerformanceLevel']", "value"), AssessmentHeaders.AssessmentClaim3PerformanceLevelIdentifier),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='ScaleScore']", "value"), AssessmentHeaders.AssessmentSubtestResultScoreClaim4Value),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='MinScore']", "value"), AssessmentHeaders.AssessmentSubtestClaim4MinimumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='MaxScore']", "value"), AssessmentHeaders.AssessmentSubtestClaim4MaximumValue),
                               Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='PerformanceLevel']", "value"), AssessmentHeaders.AssessmentClaim4PerformanceLevelIdentifier),

                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='AmericanSignLanguage']", "value", "context"), AssessmentHeaders.AccommodationAmericanSignLanguage),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='AmericanSignLanguageInterpreter']", "value", "context"), AssessmentHeaders.AccommodationSignLanguageHumanIntervention),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='Braile']", "value", "context"), AssessmentHeaders.AccommodationBraille),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='ClosedCaptioning']", "value", "context"), AssessmentHeaders.AccommodationClosedCaptioning),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='TTS']", "value", "context"), AssessmentHeaders.AccommodationTextToSpeech),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='Abacus']", "value", "context"), AssessmentHeaders.AccommodationAbacus),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='AlternateResponseOptions']", "value", "context"), AssessmentHeaders.AccommodationAlternateResponseOptions),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='Calculator']", "value", "context"), AssessmentHeaders.AccommodationCalculator),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='MultiplicationTable']", "value", "context"), AssessmentHeaders.AccommodationMultiplicationTable),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='PrintOnDemand']", "value", "context"), AssessmentHeaders.AccommodationPrintOnDemand),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='ReadAloud']", "value", "context"), AssessmentHeaders.AccommodationReadAloud),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='Scribe']", "value", "context"), AssessmentHeaders.AccommodationScribe),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='SpeechToText']", "value", "context"), AssessmentHeaders.AccommodationSpeechToText),
                               Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='StreamlineMode']", "value", "context"), AssessmentHeaders.AccommodationStreamlineMode)])
    mappings.evaluate()
    return mappings
