'''
Created on Aug 8, 2014

@author: dip
'''
from edcore.utils.utils import merge_dict
from smarter_score_batcher.utils.xml_utils import extract_meta_with_fallback_helper,\
    extract_meta_without_fallback_helper


class XMLMeta:
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
    def __init__(self, src, target):
        self.src = src
        self.target = target

    def evaluate(self):
        return {self.target: self.src.get_value()}


class CSVHeaders:
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


def get_csv_mapping(root):
    examinee = root.find("./Examinee")
    opportunity = root.find("./Opportunity")
    test_node = root.find("./Test")

    # In the order of the csv headers
    mappings = [Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='StateName']", "value", "context"), CSVHeaders.StateAbbreviation),
                Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='DistrictID']", "value", "context"), CSVHeaders.ResponsibleSchoolIdentifier),
                Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='DistrictName']", "value", "context"), CSVHeaders.OrganizationName),
                Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='SchoolID']", "value", "context"), CSVHeaders.ResponsibleSchoolIdentifier),
                Mapping(XMLMeta(examinee, "./ExamineeRelationship/[@name='SchoolName']", "value", "context"), CSVHeaders.NameOfInstitution),

                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='StudentIdentifier']", "value", "context"), CSVHeaders.StudentIdentifier),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='AlternateSSID']", "value", "context"), CSVHeaders.ExternalSSID),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='FirstName']", "value", "context"), CSVHeaders.FirstName),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='MiddleName']", "value", "context"), CSVHeaders.MiddleName),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='LastOrSurname']", "value", "context"), CSVHeaders.LastOrSurname),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Sex']", "value", "context"), CSVHeaders.Sex),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Birthdate']", "value", "context"), CSVHeaders.Birthdate),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='GradeLevelWhenAssessed']", "value", "context"), CSVHeaders.GradeLevelWhenAssessed),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='HispanicOrLatinoEthnicity']", "value", "context"), CSVHeaders.HispanicOrLatinoEthnicity),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='AmericanIndianOrAlaskaNative']", "value", "context"), CSVHeaders.AmericanIndianOrAlaskaNative),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Asian']", "value", "context"), CSVHeaders.Asian),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='BlackOrAfricanAmerican']", "value", "context"), CSVHeaders.BlackOrAfricanAmerican),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='NativeHawaiianOrOtherPacificIslander']", "value", "context"), CSVHeaders.NativeHawaiianOrOtherPacificIslander),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='White']", "value", "context"), CSVHeaders.White),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='DemographicRaceTwoOrMoreRaces']", "value", "context"), CSVHeaders.DemographicRaceTwoOrMoreRaces),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='IDEAIndicator']", "value", "context"), CSVHeaders.IDEAIndicator),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='LEPStatus']", "value", "context"), CSVHeaders.LEPStatus),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Section504Status']", "value", "context"), CSVHeaders.Section504Status),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='EconomicDisadvantageStatus']", "value", "context"), CSVHeaders.EconomicDisadvantageStatus),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='MigrantStatus']", "value", "context"), CSVHeaders.MigrantStatus),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Group1Id']", "value", "context"), CSVHeaders.Group1Id),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Group1Text']", "value", "context"), CSVHeaders.Group1Text),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Group2Id']", "value", "context"), CSVHeaders.Group2Id),
                Mapping(XMLMeta(examinee, "./ExamineeAttribute/[@name='Group2Text']", "value", "context"), CSVHeaders.Group2Text),

                Mapping(XMLMeta(test_node, ".", "testId"), CSVHeaders.AssessmentGuid),
                Mapping(XMLMeta(opportunity, ".", "oppId"), CSVHeaders.AssessmentSessionLocationId),
                Mapping(XMLMeta(opportunity, ".", "server"), CSVHeaders.AssessmentSessionLocation),
                Mapping(XMLMeta(opportunity, ".", "dateCompleted"), CSVHeaders.AssessmentAdministrationFinishDate),
                Mapping(XMLMeta(test_node, ".", "academicYear"), CSVHeaders.AssessmentYear),
                Mapping(XMLMeta(test_node, ".", "assessmentType"), CSVHeaders.AssessmentType),
                Mapping(XMLMeta(test_node, ".", "subject"), CSVHeaders.AssessmentAcademicSubject),
                Mapping(XMLMeta(test_node, ".", "grade"), CSVHeaders.AssessmentLevelForWhichDesigned),

                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='ScaleScore']", "value"), CSVHeaders.AssessmentSubtestResultScoreValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='MinScore']", "value"), CSVHeaders.AssessmentSubtestMinimumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='MaxScore']", "value"), CSVHeaders.AssessmentSubtestMaximumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Overall'][@measureLabel='PerformanceLevel']", "value"), CSVHeaders.AssessmentPerformanceLevelIdentifier),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='ScaleScore']", "value"), CSVHeaders.AssessmentSubtestResultScoreClaim1Value),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='MinScore']", "value"), CSVHeaders.AssessmentSubtestClaim1MinimumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='MaxScore']", "value"), CSVHeaders.AssessmentSubtestClaim1MaximumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim1'][@measureLabel='PerformanceLevel']", "value"), CSVHeaders.AssessmentClaim1PerformanceLevelIdentifier),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='ScaleScore']", "value"), CSVHeaders.AssessmentSubtestResultScoreClaim2Value),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='MinScore']", "value"), CSVHeaders.AssessmentSubtestClaim2MinimumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='MaxScore']", "value"), CSVHeaders.AssessmentSubtestClaim2MaximumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim2'][@measureLabel='PerformanceLevel']", "value"), CSVHeaders.AssessmentClaim2PerformanceLevelIdentifier),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='ScaleScore']", "value"), CSVHeaders.AssessmentSubtestResultScoreClaim3Value),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='MinScore']", "value"), CSVHeaders.AssessmentSubtestClaim3MinimumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='MaxScore']", "value"), CSVHeaders.AssessmentSubtestClaim3MaximumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim3'][@measureLabel='PerformanceLevel']", "value"), CSVHeaders.AssessmentClaim3PerformanceLevelIdentifier),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='ScaleScore']", "value"), CSVHeaders.AssessmentSubtestResultScoreClaim4Value),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='MinScore']", "value"), CSVHeaders.AssessmentSubtestClaim4MinimumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='MaxScore']", "value"), CSVHeaders.AssessmentSubtestClaim4MaximumValue),
                Mapping(XMLMeta(opportunity, "./Score/[@measureOf='Claim4'][@measureLabel='PerformanceLevel']", "value"), CSVHeaders.AssessmentClaim4PerformanceLevelIdentifier),

                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='AmericanSignLanguage']", "value", "context"), CSVHeaders.AccommodationAmericanSignLanguage),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='AmericanSignLanguageInterpreter']", "value", "context"), CSVHeaders.AccommodationSignLanguageHumanIntervention),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='Braile']", "value", "context"), CSVHeaders.AccommodationBraille),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='ClosedCaptioning']", "value", "context"), CSVHeaders.AccommodationClosedCaptioning),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='TTS']", "value", "context"), CSVHeaders.AccommodationTextToSpeech),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='Abacus']", "value", "context"), CSVHeaders.AccommodationAbacus),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='AlternateResponseOptions']", "value", "context"), CSVHeaders.AccommodationAlternateResponseOptions),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='Calculator']", "value", "context"), CSVHeaders.AccommodationCalculator),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='MultiplicationTable']", "value", "context"), CSVHeaders.AccommodationMultiplicationTable),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='PrintOnDemand']", "value", "context"), CSVHeaders.AccommodationPrintOnDemand),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='ReadAloud']", "value", "context"), CSVHeaders.AccommodationReadAloud),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='Scribe']", "value", "context"), CSVHeaders.AccommodationScribe),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='SpeechToText']", "value", "context"), CSVHeaders.AccommodationSpeechToText),
                Mapping(AccommodationMeta(opportunity, "./Accommodation/[@type='StreamlineMode']", "value", "context"), CSVHeaders.AccommodationStreamlineMode)]

    values = {}
    for m in mappings:
        values = merge_dict(values, m.evaluate())
    return values
