__author__ = 'sravi'

import unittest
from unittest.mock import patch, MagicMock
from edudl2.exceptions.errorcodes import ErrorCode
from edudl2.content_validator.content_validator import ContentValidator, ISValidAssessmentPair


class TestContentValidator(unittest.TestCase):

    def setUp(self):
        pass

    @patch('edudl2.content_validator.content_validator.ISValidAssessmentPair')
    def test_content_validator_execute_for_invalid_file_pair(self, mock_is_valid_assessment_pair):
        mock_instance = mock_is_valid_assessment_pair.return_value
        mock_instance.execute.return_value = ErrorCode.ASMT_GUID_MISMATCH_IN_JSON_CSV_PAIR
        validator = ContentValidator()
        validator.validators = [mock_instance]
        error_list = validator.execute(conf={})
        self.assertEqual(len(error_list), 1)
        self.assertEqual(error_list, [ErrorCode.ASMT_GUID_MISMATCH_IN_JSON_CSV_PAIR])

    @patch('edudl2.content_validator.content_validator.ISValidAssessmentPair')
    def test_content_validator_execute_for_valid_file_pair(self, mock_is_valid_assessment_pair):
        mock_instance = mock_is_valid_assessment_pair.return_value
        mock_instance.execute.return_value = ErrorCode.STATUS_OK
        validator = ContentValidator()
        validator.validators = [mock_instance]
        error_list = validator.execute(conf={})
        self.assertEqual(len(error_list), 0)

    def test_content_validator_execute_for_no_validators(self):
        validator = ContentValidator()
        validator.validators = None
        error_list = validator.execute(conf={})
        self.assertEqual(len(error_list), 0)
        validator.validators = []
        error_list = validator.execute(conf={})
        self.assertEqual(len(error_list), 0)

    @patch('edudl2.content_validator.content_validator.ISValidAssessmentPair')
    @patch('edudl2.content_validator.content_validator.ISValidAssessmentPair')
    def test_content_validator_execute_for_multiple_validators_some_fail(self, mock_is_valid_assessment_pair_1,
                                                               mock_is_valid_assessment_pair_2):
        mock_instance_1 = mock_is_valid_assessment_pair_1.return_value
        mock_instance_1.execute.return_value = ErrorCode.STATUS_OK
        mock_instance_2 = mock_is_valid_assessment_pair_2.return_value
        mock_instance_2.execute.return_value = ErrorCode.ASMT_GUID_MISMATCH_IN_JSON_CSV_PAIR
        validator = ContentValidator()
        validator.validators = [mock_instance_1, mock_instance_2]
        error_list = validator.execute(conf={})
        self.assertEqual(len(error_list), 1)
        self.assertEqual(error_list, [ErrorCode.ASMT_GUID_MISMATCH_IN_JSON_CSV_PAIR])

    @patch('edudl2.content_validator.content_validator.ISValidAssessmentPair')
    @patch('edudl2.content_validator.content_validator.ISValidAssessmentPair')
    def test_content_validator_execute_for_multiple_validators_all_pass(self, mock_is_valid_assessment_pair_1,
                                                                        mock_is_valid_assessment_pair_2):
        mock_instance_1 = mock_is_valid_assessment_pair_1.return_value
        mock_instance_1.execute.return_value = ErrorCode.STATUS_OK
        mock_instance_2 = mock_is_valid_assessment_pair_2.return_value
        mock_instance_2.execute.return_value = ErrorCode.STATUS_OK
        validator = ContentValidator()
        validator.validators = [mock_instance_1, mock_instance_2]
        error_list = validator.execute(conf={})
        self.assertEqual(len(error_list), 0)

    @patch.object(ISValidAssessmentPair, 'get_asmt_and_outcome_result')
    def test_is_valid_assessment_pair_for_valid_json_csv_file_combination(self, mock_get_asmt_and_outcome_result):
        mock_get_asmt_and_outcome_result.return_value = ([dict({'guid_asmt': '123'})], [dict({'guid_asmt': '123'})])
        is_valid_assessment_pair = ISValidAssessmentPair()
        error_code = is_valid_assessment_pair.execute(conf={})
        is_valid_assessment_pair.get_asmt_and_outcome_result.assert_called_once_with({})
        self.assertEqual(error_code, ErrorCode.STATUS_OK)

    @patch.object(ISValidAssessmentPair, 'get_asmt_and_outcome_result')
    def test_is_valid_assessment_pair_for_invalid_file_combination(self, mock_get_asmt_and_outcome_result):
        mock_get_asmt_and_outcome_result.return_value = ([dict({'guid_asmt': '123'})], [dict({'guid_asmt': '130'})])
        is_valid_assessment_pair = ISValidAssessmentPair()
        error_code = is_valid_assessment_pair.execute(conf={})
        is_valid_assessment_pair.get_asmt_and_outcome_result.assert_called_once_with({})
        self.assertEqual(error_code, ErrorCode.ASMT_GUID_MISMATCH_IN_JSON_CSV_PAIR)

    @patch.object(ISValidAssessmentPair, 'get_asmt_and_outcome_result')
    def test_is_valid_assessment_pair_for_csv_with_multiple_asmnts(self, mock_get_asmt_and_outcome_result):
        mock_get_asmt_and_outcome_result.return_value = ([dict({'guid_asmt': '123'})], [dict({'guid_asmt': '130'}), dict({'guid_asmt': '123'})])
        is_valid_assessment_pair = ISValidAssessmentPair()
        error_code = is_valid_assessment_pair.execute(conf={})
        is_valid_assessment_pair.get_asmt_and_outcome_result.assert_called_once_with({})
        self.assertEqual(error_code, ErrorCode.ASMT_GUID_MISMATCH_IN_JSON_CSV_PAIR)

    @patch.object(ISValidAssessmentPair, 'get_asmt_and_outcome_result')
    def test_is_valid_assessment_pair_for_csv_with_no_asmnts(self, mock_get_asmt_and_outcome_result):
        mock_get_asmt_and_outcome_result.return_value = ([dict({'guid_asmt': '123'})], [])
        is_valid_assessment_pair = ISValidAssessmentPair()
        error_code = is_valid_assessment_pair.execute(conf={})
        is_valid_assessment_pair.get_asmt_and_outcome_result.assert_called_once_with({})
        self.assertEqual(error_code, ErrorCode.ASMT_GUID_MISMATCH_IN_JSON_CSV_PAIR)
