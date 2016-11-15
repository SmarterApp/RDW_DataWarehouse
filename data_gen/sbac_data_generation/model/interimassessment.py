# -*- coding: utf-8 -*-
"""
Model an interim assessment for the SBAC assessment.

@author: mjacob
@date: October 22, 2014
"""

import data_generation.writers.filters as write_filters
import sbac_data_generation.config.cfg as sbac_config

from data_generation.model.assessment import Assessment


class SBACInterimAssessment(Assessment):
    """
    The SBAC-specific interim assessment class.
    """

    # mjacob: using slots here only to avoid bugs due to typos etc.
    __slots__ = ('run_id', 'guid',  # inherited from AssessmentOutcome
                 'rec_id', 'guid_sr', 'asmt_type', 'period', 'period_year', 'version', 'subject',
                 'claim_1_name', 'claim_2_name', 'claim_3_name', 'claim_4_name',
                 'perf_lvl_name_1', 'perf_lvl_name_2', 'perf_lvl_name_3', 'perf_lvl_name_4', 'perf_lvl_name_5',
                 'overall_score_min', 'claim_1_score_min', 'claim_2_score_min', 'claim_3_score_min', 'claim_4_score_min',
                 'overall_score_max', 'claim_1_score_max', 'claim_2_score_max', 'claim_3_score_max', 'claim_4_score_max',
                 'claim_1_score_weight', 'claim_2_score_weight', 'claim_3_score_weight', 'claim_4_score_weight',
                 'claim_perf_lvl_name_1', 'claim_perf_lvl_name_2', 'claim_perf_lvl_name_3',
                 'overall_cut_point_1', 'overall_cut_point_2', 'overall_cut_point_3', 'overall_cut_point_4',
                 'claim_cut_point_1', 'claim_cut_point_2',
                 'from_date', 'to_date', 'effective_date', 'item_bank',)

    def __init__(self):
        super().__init__()
        self.rec_id = None
        self.guid_sr = None
        self.asmt_type = None
        self.period = None
        self.period_year = None
        self.version = None
        self.subject = None
        self.claim_1_name = None
        self.claim_2_name = None
        self.claim_3_name = None
        self.claim_4_name = None
        self.perf_lvl_name_1 = None
        self.perf_lvl_name_2 = None
        self.perf_lvl_name_3 = None
        self.perf_lvl_name_4 = None
        self.perf_lvl_name_5 = None
        self.overall_score_min = None
        self.overall_score_max = None
        self.claim_1_score_min = None
        self.claim_1_score_max = None
        self.claim_1_score_weight = None
        self.claim_2_score_min = None
        self.claim_2_score_max = None
        self.claim_2_score_weight = None
        self.claim_3_score_min = None
        self.claim_3_score_max = None
        self.claim_3_score_weight = None
        self.claim_4_score_min = None
        self.claim_4_score_max = None
        self.claim_4_score_weight = None
        self.claim_perf_lvl_name_1 = None
        self.claim_perf_lvl_name_2 = None
        self.claim_perf_lvl_name_3 = None
        self.overall_cut_point_1 = None
        self.overall_cut_point_2 = None
        self.overall_cut_point_3 = None
        self.overall_cut_point_4 = None
        self.claim_cut_point_1 = None
        self.claim_cut_point_2 = None
        self.from_date = sbac_config.HIERARCHY_FROM_DATE
        self.to_date = None
        self.effective_date = None
        self.item_bank = None

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        Root objects made available:
          - assessment

        :returns: Dictionary of root objects
        """
        return {'assessment': self,
                'assessment_effective': {'date': write_filters.filter_date_Ymd(self.effective_date)}}

    def __setattr__(self, name, value):
        """
        Prevent setting some values to prevent bugs due to typos etc.
        :param name:
        :param value:
        :return:
        """
        if name in {'overall_score_min', 'overall_score_max',
                    'overall_cut_point_1', 'overall_cut_point_2', 'overall_cut_point_3', 'overall_cut_point_4',
                    'perf_lvl_name_1', 'perf_lvl_name_2', 'perf_lvl_name_3', 'perf_lvl_name_4',
                    'claim_1_score_weight',
                    'claim_2_name', 'claim_2_score_min', 'claim_2_score_max', 'claim_2_score_weight',
                    'claim_3_name', 'claim_3_score_min', 'claim_3_score_max', 'claim_3_score_weight',
                    'claim_4_name', 'claim_4_score_min', 'claim_4_score_max', 'claim_4_score_weight', }:
            raise AttributeError('cannot set %s of %s' % (name, self.__class__.__qualname__))

        else:
            super().__setattr__(name, value)
