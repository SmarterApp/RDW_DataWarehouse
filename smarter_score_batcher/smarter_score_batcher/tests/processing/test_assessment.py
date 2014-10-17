'''
Created on Aug 12, 2014

@author: dip
'''
import unittest
from smarter_score_batcher.processing.assessment import XMLMeta, Mapping,\
    get_assessment_mapping, AssessmentHeaders, AssessmentData,\
    getClaimMappingName
from smarter_score_batcher.tests.processing.utils import DummyObj, read_data
import os
import json
from smarter_score_batcher.utils.constants import PerformanceMetadataConstants
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class TestCSVMetadata(unittest.TestCase):

    def test_xml_metadata_with_attribute_in_node(self):
        data = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        </TDSReport>'''
        root = ET.fromstring(data)
        xmlmeta = XMLMeta(root, './Test', 'grade')
        val = xmlmeta.get_value()
        self.assertEquals(val, '3-12')

    def test_xml_metadata_with_attribute_to_compare(self):
        data = '''<TDSReport>
        <Accommodation type="Speech to Text" value="9" context="FINAL" />
        </TDSReport>'''
        root = ET.fromstring(data)
        xmlmeta = XMLMeta(root, "./Accommodation/[@type='Speech to Text']", 'value', 'context')
        val = xmlmeta.get_value()
        self.assertEquals(val, '9')

    def test_mapping_class(self):
        mapping = Mapping(DummyObj(), 'test')
        val = mapping.evaluate()
        self.assertEquals(val, 1)

    def test_get_csv_mapping(self):
        here = os.path.abspath(os.path.dirname(__file__))
        static_metadata = os.path.join(here, '..', 'resources', 'meta', 'static', 'ELA.static_asmt_metadata.json')
        data = read_data("assessment.xml")
        root = ET.fromstring(data)
        data = get_assessment_mapping(root, static_metadata)
        header = data.header
        values = data.values
        self.assertEqual(len(header), len(values))
        self.assertTrue(len(header) > 0)
        mapping = dict(zip(header, values))
        self.assertEqual(mapping[AssessmentHeaders.AssessmentGuid], 'SBAC-FT-SomeDescription-ELA-7')
        self.assertEqual(mapping[AssessmentHeaders.AccommodationBraille], None)
        self.assertEqual(mapping[AssessmentHeaders.StudentIdentifier], '922171')
        self.assertEqual(mapping[AssessmentHeaders.Asian], 'No')
        self.assertEqual(mapping[AssessmentHeaders.ResponsibleSchoolIdentifier], 'CA_9999827_9999928')
        self.assertEqual(mapping[AssessmentHeaders.NameOfInstitution], 'My Elementary School')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSessionLocationId], '1855629')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSessionLocation], '562299-SBASQL8')
        self.assertEqual(mapping[AssessmentHeaders.AccommodationAmericanSignLanguage], '6')
        self.assertEqual(mapping[AssessmentHeaders.Birthdate], '20130831')
        self.assertEqual(mapping[AssessmentHeaders.StateAbbreviation], 'CA')
        self.assertEqual(mapping[AssessmentHeaders.ResponsibleDistrictIdentifier], 'CA_9999827')
        self.assertEqual(mapping[AssessmentHeaders.OrganizationName], 'This Elementary School District')
        self.assertEqual(mapping[AssessmentHeaders.ExternalSSID], 'CA-9999999598')
        self.assertEqual(mapping[AssessmentHeaders.FirstName], 'John')
        self.assertEqual(mapping[AssessmentHeaders.LastOrSurname], 'Smith')
        self.assertEqual(mapping[AssessmentHeaders.Sex], 'Male')
        self.assertEqual(mapping[AssessmentHeaders.GradeLevelWhenAssessed], '3')
        self.assertEqual(mapping[AssessmentHeaders.HispanicOrLatinoEthnicity], 'No')
        self.assertEqual(mapping[AssessmentHeaders.AmericanIndianOrAlaskaNative], 'No')
        self.assertEqual(mapping[AssessmentHeaders.Asian], 'No')
        self.assertEqual(mapping[AssessmentHeaders.BlackOrAfricanAmerican], 'Yes')
        self.assertEqual(mapping[AssessmentHeaders.NativeHawaiianOrOtherPacificIslander], 'No')
        self.assertEqual(mapping[AssessmentHeaders.White], 'No')
        self.assertEqual(mapping[AssessmentHeaders.DemographicRaceTwoOrMoreRaces], 'No')
        self.assertEqual(mapping[AssessmentHeaders.IDEAIndicator], 'No')
        self.assertEqual(mapping[AssessmentHeaders.LEPStatus], 'Yes')
        self.assertEqual(mapping[AssessmentHeaders.Section504Status], 'No')
        self.assertEqual(mapping[AssessmentHeaders.EconomicDisadvantageStatus], 'No')
        self.assertEqual(mapping[AssessmentHeaders.MigrantStatus], 'Yes')
        # test groups
        self.assertEqual(mapping[AssessmentHeaders.Group1Id], 'Brennan Math')
        self.assertEqual(mapping[AssessmentHeaders.Group1Text], 'Brennan Math')
        self.assertEqual(mapping[AssessmentHeaders.Group2Id], 'Tuesday Science')
        self.assertEqual(mapping[AssessmentHeaders.Group2Text], 'Tuesday Science')
        self.assertEqual(mapping[AssessmentHeaders.Group3Id], 'Smith Research')
        self.assertEqual(mapping[AssessmentHeaders.Group3Text], 'Smith Research')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentAdministrationFinishDate], '20140414')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentYear], '2014')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentType], 'Summative')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentLevelForWhichDesigned], '3')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestResultScoreValue], '245.174914080214')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestMinimumValue], '226')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestMaximumValue], '264')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentPerformanceLevelIdentifier], '2')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestResultScoreClaim1Value], '352.897')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestClaim1MinimumValue], '-267')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestClaim1MaximumValue], '971')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentClaim1PerformanceLevelIdentifier], '2')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestResultScoreClaim2Value], '185.002')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestClaim2MinimumValue], '107')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestClaim2MaximumValue], '263')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentClaim2PerformanceLevelIdentifier], '1')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestResultScoreClaim3Value], '403.416')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestClaim3MinimumValue], '199')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestClaim3MaximumValue], '607')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentClaim3PerformanceLevelIdentifier], '2')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestResultScoreClaim4Value], '403.416')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestClaim4MinimumValue], '199')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentSubtestClaim4MaximumValue], '607')
        self.assertEqual(mapping[AssessmentHeaders.AssessmentClaim4PerformanceLevelIdentifier], '2')

    def test_assessment_data_class(self):
        data = AssessmentData([Mapping(DummyObj(), "test_header")])
        data.evaluate()
        self.assertListEqual(data.header, ['test_header'])
        self.assertListEqual(data.values, [1])

    def test_getClaimMappingName(self):
        here = os.path.abspath(os.path.dirname(__file__))
        static_metadata = os.path.join(here, '..', 'resources', 'meta', 'static', 'MATH.static_asmt_metadata.json')
        with open(static_metadata) as f:
            metadata_string = f.read()
            metadata = json.loads(metadata_string)
        mapping = getClaimMappingName(metadata, 'hello', 'world')
        self.assertEqual(mapping, 'world')
        mapping = getClaimMappingName(metadata, PerformanceMetadataConstants.CLAIM2, 'world')
        self.assertEqual(mapping, 'Claim2Problem Solving and Modeling & Data Analysis')
        mapping = getClaimMappingName(None, PerformanceMetadataConstants.CLAIM2, 'world')
        self.assertEqual(mapping, 'world')

if __name__ == "__main__":
    unittest.main()
