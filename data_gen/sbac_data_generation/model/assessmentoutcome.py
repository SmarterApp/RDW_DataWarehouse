"""
Model an assessment outcome (an instance of a student taking an assessment) for the SBAC assessment.

@author: nestep
@date: March 3, 2014
"""

import datetime

from data_generation.model.assessmentoutcome import AssessmentOutcome

import sbac_data_generation.config.cfg as sbac_config


class SBACAssessmentOutcome(AssessmentOutcome):
    """
    The SBAC-specific assessment outcome class.
    """
    def __init__(self):
        super().__init__()
        self.rec_id = None
        self.inst_hierarchy = None
        self.result_status = sbac_config.ASMT_STATUS_ACTIVE
        self.overall_score = None
        self.overall_score_range_min = None
        self.overall_score_range_max = None
        self.overall_perf_lvl = None
        self.claim_1_score = None
        self.claim_1_score_range_min = None
        self.claim_1_score_range_max = None
        self.claim_1_perf_lvl = None
        self.claim_2_score = None
        self.claim_2_score_range_min = None
        self.claim_2_score_range_max = None
        self.claim_2_perf_lvl = None
        self.claim_3_score = None
        self.claim_3_score_range_min = None
        self.claim_3_score_range_max = None
        self.claim_3_perf_lvl = None
        self.claim_4_score = None
        self.claim_4_score_range_min = None
        self.claim_4_score_range_max = None
        self.claim_4_perf_lvl = None
        self.acc_asl_video_embed = 0
        self.acc_asl_human_nonembed = 0
        self.acc_braile_embed = 0
        self.acc_closed_captioning_embed = 0
        self.acc_text_to_speech_embed = 0
        self.acc_abacus_nonembed = 0
        self.acc_alternate_response_options_nonembed = 0
        self.acc_calculator_nonembed = 0
        self.acc_multiplication_table_nonembed = 0
        self.acc_print_on_demand_nonembed = 0
        self.acc_read_aloud_nonembed = 0
        self.acc_scribe_nonembed = 0
        self.acc_speech_to_text_nonembed = 0
        self.acc_streamline_mode = 0
        self.from_date = sbac_config.HIERARCHY_FROM_DATE
        self.to_date = datetime.date(9999, 12, 31)
        self.item_level_data = []
        self.group_1_id = None
        self.group_1_text = None
        self.group_2_id = None
        self.group_2_text = None

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
