"""
Go through and calculate the average students sizes for the different state types in the system.

@author: nestep
@date: March 20, 2014
"""

import data_generation.config.hierarchy as hier_config
import data_generation.util.hiearchy as hier_util
import sbac_data_generation.config.hierarchy as sbac_hier_config

# Extend general configuration dictionary with SBAC-specific configs
hier_config.SCHOOL_TYPES.update(sbac_hier_config.SCHOOL_TYPES)
hier_config.DISTRICT_TYPES.update(sbac_hier_config.DISTRICT_TYPES)
hier_config.STATE_TYPES.update(sbac_hier_config.STATE_TYPES)

if __name__ == '__main__':
    for state_type, state_config in hier_config.STATE_TYPES.items():
        print('Calculating for type: %s' % state_type)

        state_student_count = 0
        state_school_count = 0
        state_district_count = 0
        for district_type, district_count in state_config['district_types_and_counts'].items():
            # Get the district config
            district_config = hier_config.DISTRICT_TYPES[district_type]
            avg_school_count = district_config['school_counts']['avg']

            # Convert school type counts into decimal ratios
            hier_util.convert_config_school_count_to_ratios(district_config)

            # Go through each, calculate how many (on average) and the number of students in that school
            district_student_count = 0
            for school_type, school_ratio in district_config['school_types_and_ratios'].items():
                # Get the school config
                school_config = hier_config.SCHOOL_TYPES[school_type]
                avg_student_count = school_config['students']['avg']

                # Determine the number of schools that will be created for this district (on average)
                num_schools_for_district = max(1, int(avg_school_count * school_ratio))

                # Determine the average number of students in this school
                school_student_count = 0
                for grade in school_config['grades']:
                    school_student_count += avg_student_count

                # Add to the district total
                district_student_count += school_student_count * num_schools_for_district

            # Add to the state totals
            state_student_count += district_student_count * district_count
            state_school_count += avg_school_count * district_count
            state_district_count += district_count

        print('    Districts: %i' % state_district_count)
        print('    Schools  : %i' % state_school_count)
        print('    Students : %i' % state_student_count)