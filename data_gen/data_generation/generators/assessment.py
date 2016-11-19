"""Generate assessment elements.

"""
from data_generation.util.id_gen import IDGen as id_gen

from data_generation.model.assessment import Assessment
from data_generation.model.assessmentoutcome import AssessmentOutcome
from data_generation.model.student import Student


def generate_assessment(sub_class=None):
    """Generate a data_generation assessment.

    :param sub_class: The sub-class of assessment to create (if requested, must be subclass of Assessment)
    :returns: The assessment object
    """
    # Create the object
    a = Assessment() if sub_class is None else sub_class()
    a.guid = id_gen.get_uuid()

    return a


def generate_assessment_outcome(student: Student, assessment: Assessment, sub_class=None):
    """Generate an assessment outcome for a given student.

    :param student: The student to create the outcome for
    :param assessment: The assessment to create the outcome for
    :param sub_class: The sub-class of assessment outcome to create (if requested, must be subclass of
                      AssessmentOutcome)
    :returns: The assessment outcome
    """
    # Create the object
    ao = AssessmentOutcome() if sub_class is None else sub_class()
    ao.guid = id_gen.get_uuid()
    ao.student = student
    ao.assessment = assessment

    return ao
