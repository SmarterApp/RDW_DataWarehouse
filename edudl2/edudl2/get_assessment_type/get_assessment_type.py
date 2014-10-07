import logging
from edudl2.json_util.json_util import get_value_from_json
from edudl2.udl2.constants import Constants

logger = logging.getLogger(__name__)
assessment_types = Constants.ASSESSMENT_TYPES()


def get_load_type(json_file_dir):
    """
    Get the assessment type for this UDL job from the json file
    @param json_file_dir: A directory that houses the json file
    @return: UDL job assessment type
    @rtype: string
    """

    assessment_type = get_value_from_json(json_file_dir, Constants.ASSESSMENT_TYPE_KEY).lower()

    if assessment_type not in assessment_types:
        raise ValueError('No valid load type specified in json file --')

    return assessment_type
