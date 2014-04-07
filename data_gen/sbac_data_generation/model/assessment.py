"""
Model an assessment for the SBAC assessment.

@author: nestep
@date: February 24, 2014
"""

from mongoengine import DateTimeField, FloatField, IntField, StringField

import data_generation.writers.filters as write_filters
import sbac_data_generation.config.cfg as sbac_config

from data_generation.model.assessment import Assessment


class SBACAssessment(Assessment):
    """
    The SBAC-specific assessment class.
    """
    rec_id = IntField(required=True)
    asmt_type = StringField(required=True)
    period = StringField(required=True)
    period_year = IntField(required=True)
    version = StringField(required=True)
    subject = StringField(required=True)
    claim_1_name = StringField(required=True)
    claim_2_name = StringField(required=True)
    claim_3_name = StringField(required=True)
    claim_4_name = StringField(required=False)
    perf_lvl_name_1 = StringField(required=True)
    perf_lvl_name_2 = StringField(required=True)
    perf_lvl_name_3 = StringField(required=True)
    perf_lvl_name_4 = StringField(required=True)
    perf_lvl_name_5 = StringField(required=False)
    overall_score_min = IntField(required=True)
    overall_score_max = IntField(required=True)
    claim_1_score_min = IntField(required=True)
    claim_1_score_max = IntField(required=True)
    claim_1_score_weight = FloatField(required=True)
    claim_2_score_min = IntField(required=True)
    claim_2_score_max = IntField(required=True)
    claim_2_score_weight = FloatField(required=True)
    claim_3_score_min = IntField(required=True)
    claim_3_score_max = IntField(required=True)
    claim_3_score_weight = FloatField(required=True)
    claim_4_score_min = IntField(required=False)
    claim_4_score_max = IntField(required=False)
    claim_4_score_weight = FloatField(required=False)
    claim_perf_lvl_name_1 = StringField(required=True)
    claim_perf_lvl_name_2 = StringField(required=True)
    claim_perf_lvl_name_3 = StringField(required=True)
    overall_cut_point_1 = IntField(required=True)
    overall_cut_point_2 = IntField(required=True)
    overall_cut_point_3 = IntField(required=True)
    overall_cut_point_4 = IntField(required=False)
    claim_cut_point_1 = IntField(required=True)
    claim_cut_point_2 = IntField(required=True)
    from_date = DateTimeField(required=True, default=sbac_config.HIERARCHY_FROM_DATE)
    to_date = DateTimeField(required=False)
    effective_date = DateTimeField(required=False)

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        Root objects made available:
          - assessment

        :returns: Dictionary of root objects
        """
        return {'assessment': self,
                'assessment_effective': {'date': write_filters.filter_date_Ymd(self.effective_date)}}
