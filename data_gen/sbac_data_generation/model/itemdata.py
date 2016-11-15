"""
Model an item data generated for an assessment outcome (an instance of a student taking an assessment) for the SBAC assessment.

@author: gkathuria
@date: May 16, 2014
"""


class SBACAssessmentOutcomeItemData:
    """
    The SBAC-specific assessment outcome Item Data class.
    """
    def __init__(self):
        self.student_id = None
        self.key = None
        self.segment_id = None
        self.position = None
        self.client_id = None
        self.operational = None
        self.is_selected = None
        self.format = None
        self.score = None
        self.score_status = None
        self.admin_date = None
        self.number_visits = None
        self.strand = None
        self.content_level = None
        self.page_number = None
        self.page_visits = None
        self.page_time = None
        self.dropped = None

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'assessment_outcome_item_data': self}
