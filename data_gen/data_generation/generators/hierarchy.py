"""Generate hierarchy components.

:author: nestep
:date: Febraury 21, 2014
"""

import data_generation.config.hierarchy as hier_config
import data_generation.config.population as pop_config
import data_generation.generators.names as name_gen
from data_generation.util.id_gen import IDGen as id_gen
from data_generation.model.district import District
from data_generation.model.school import School
from data_generation.model.state import State


def generate_state(state_type, name, code, state_types=hier_config.STATE_TYPES, pop_demos=pop_config.DEMOGRAPHICS,
                   sub_class=None):
    """Generate a state of the given state type.

    :param state_type: The type of state to generate
    :param name: The name of the state
    :param code: The two-character code of the state
    :param state_types: The state types configuration object
    :param pop_demos: The population demographics configuration object
    :param sub_class: The sub-class of state to create (if requested, must be subclass of State)
    :returns: The state
    """
    # Validate state type
    if state_type not in state_types:
        raise LookupError("State type '" + str(state_type) + "' was not found")

    # Create the state
    s = State() if sub_class is None else sub_class()
    s.guid = id_gen.get_uuid()
    s.name = name
    s.code = code
    s.type_str = state_type
    s.config = state_types[state_type]

    # Validate the demographics type
    if s.config['demographics'] not in pop_config.DEMOGRAPHICS:
        raise LookupError("Demographics type '" + str(s.config['demographics']) + "' was not found")

    # Store the demographics
    s.demo_config = pop_demos[s.config['demographics']]

    return s


def generate_district(district_type, state: State, district_types=hier_config.DISTRICT_TYPES, sub_class=None):
    """Generate a district specified by the parameters.

    :param district_type: The type of district to generate
    :param state: The state the district belongs to
    :param district_types: The district types configuration object
    :param sub_class: The sub-class of district to create (if requested, must be subclass of District)
    :returns: The district
    """
    # Validate state type
    if district_type not in district_types:
        raise LookupError("District type '" + str(district_type) + "' was not found")

    # Create and store the district
    d = District() if sub_class is None else sub_class()
    d.guid = id_gen.get_uuid()
    d.name = name_gen.generate_district_name()
    d.state = state
    d.type_str = district_type
    d.config = district_types[district_type]
    d.demo_config = state.demo_config

    return d


def generate_school(school_type, district: District, school_types=hier_config.SCHOOL_TYPES, sub_class=None):
    """Generate a school specified by the parameters.

    :param school_type: The type of school to generate
    :param district: The district the school belongs to
    :param school_types: The school types configuration object
    :param sub_class: The sub-class of school to create (if requested, must be subclass of School)
    :returns: The school
    """
    # Validate the school type
    if school_type not in school_types:
        raise LookupError("School type '" + str(school_type) + "' was not found")

    # Create and store the school
    s = School() if sub_class is None else sub_class()
    s.guid = id_gen.get_uuid()
    s.name = name_gen.generate_school_name(hier_config.SCHOOL_TYPES[school_type]['type'])
    s.district = district
    s.type_str = school_type
    s.config = school_types[school_type]
    s.demo_config = district.demo_config

    return s
