"""
Model an assessment outcome (an instance of a student taking an assessment) for the SBAC assessment.

@author: nestep
@date: March 3, 2014
"""

import datetime

from mongoengine import DateTimeField, IntField, ReferenceField, StringField

import sbac_data_generation.config.cfg as sbac_config

from data_generation.model.assessmentoutcome import AssessmentOutcome
from sbac_data_generation.model.institutionhierarchy import InstitutionHierarchy


class SBACAssessmentOutcome(AssessmentOutcome):
    """
    The SBAC-specific assessment outcome class.
    """
    rec_id = IntField(required=True)
    inst_hierarchy = ReferenceField(InstitutionHierarchy, required=True)
    result_status = StringField(required=True, default=sbac_config.ASMT_STATUS_ACTIVE)
    overall_score = IntField(required=True, min_value=sbac_config.ASMT_SCORE_MIN,
                             max_value=sbac_config.ASMT_SCORE_MAX)
    overall_score_range_min = IntField(required=True, min_value=sbac_config.ASMT_SCORE_MIN,
                                       max_value=sbac_config.ASMT_SCORE_MAX)
    overall_score_range_max = IntField(required=True, min_value=sbac_config.ASMT_SCORE_MIN,
                                       max_value=sbac_config.ASMT_SCORE_MAX)
    overall_perf_lvl = IntField(required=True, min_value=1, max_value=5)
    claim_1_score = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                             max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_1_score_range_min = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                                       max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_1_score_range_max = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                                       max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_1_perf_lvl = IntField(required=True, min_value=1, max_value=5)
    claim_2_score = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                             max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_2_score_range_min = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                                       max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_2_score_range_max = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                                       max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_2_perf_lvl = IntField(required=True, min_value=1, max_value=5)
    claim_3_score = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                             max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_3_score_range_min = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                                       max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_3_score_range_max = IntField(required=True, min_value=sbac_config.CLAIM_SCORE_MIN,
                                       max_value=sbac_config.CLAIM_SCORE_MAX)
    claim_3_perf_lvl = IntField(required=True, min_value=1, max_value=5)
    claim_4_score = IntField(required=True, default=0)
    claim_4_score_range_min = IntField(required=True, default=0)
    claim_4_score_range_max = IntField(required=True, default=0)
    claim_4_perf_lvl = IntField(required=True, min_value=0, max_value=5, default=0)
    acc_asl_video_embed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_asl_human_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_braile_embed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_closed_captioning_embed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_text_to_speech_embed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_abacus_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_alternate_response_options_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_calculator_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_multiplication_table_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_print_on_demand_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_read_aloud_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_scribe_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_speech_to_text_nonembed = IntField(required=True, default=0, min_value=0, max_value=10)
    acc_streamline_mode = IntField(required=True, default=0, min_value=0, max_value=10)
    from_date = DateTimeField(required=True, default=sbac_config.HIERARCHY_FROM_DATE)
    to_date = DateTimeField(required=True, default=datetime.date(9999, 12, 31))

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'state': self.inst_hierarchy.state,
                'district': self.student.school.district,
                'school': self.student.school,
                'student': self.student,
                'institution_hierarchy': self.inst_hierarchy,
                'assessment': self.assessment,
                'assessment_outcome': self}
