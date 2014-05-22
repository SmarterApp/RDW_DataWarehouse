"""
Model an item data generated for an assessment outcome (an instance of a student taking an assessment) for the SBAC assessment.

@author: gkathuria
@date: May 16, 2014
"""

from mongoengine import ReferenceField, Document, EmbeddedDocument, IntField, StringField, DateTimeField


class SBACAssessmentOutcomeItemData(EmbeddedDocument):
    """
    The SBAC-specific assessment outcome Item Data class.
    """
    # assessment_outcome = ReferenceField(SBACAssessmentOutcome, required=True)
    student_guid = StringField(required=True)
    key = IntField(required=True)
    segment_id = StringField(required=True)
    position = IntField(required=True)
    client_id = StringField(required=False)
    operational = IntField(required=False)
    is_selected = IntField(required=False)
    format = StringField(required=True)
    score = IntField(required=False)
    score_status = IntField(required=False)
    admin_date = DateTimeField(required=False)
    number_visits = IntField(required=False)
    strand = StringField(required=False)
    content_level = StringField(required=False)
    page_number = IntField(required=False)
    page_visits = IntField(required=False)
    page_time = IntField(required=False)
    dropped = IntField(required=False)

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'assessment_outcome_item_data': self}
