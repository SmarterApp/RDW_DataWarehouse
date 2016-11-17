"""This module provides utility functions for hierarchy operations.

:author: nestep
:date: March 5, 2014
"""


def convert_config_school_count_to_ratios(config):
    """Take a district type hierarchy configuration and convert the school counts to decimal ratios. The configuration
    settings are manipulated in place.

    :param config: The district type configuration to manipulate
    """
    # Count the total number of schools that make up the ratio
    ratio_count = 0
    for st, count in config['school_types_and_ratios'].items():
        if count < 1:
            return  # This function has already been run on this configuration block
        ratio_count += count

    # Convert each count to decimal ratio
    for st, count in config['school_types_and_ratios'].items():
        config['school_types_and_ratios'][st] = count / ratio_count
