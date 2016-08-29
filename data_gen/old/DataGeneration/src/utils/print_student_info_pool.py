'''
Created on Aug 13, 2013

@author: swimberly
'''


def print_student_info_pool_counts(student_info_dict, demographics_info, demographics_id):
    '''
    Print out the counts of each demographic item in the student_info
    '''

    for grade in student_info_dict:
        grade_demo_percentages = demographics_info.get_grade_demographics(demographics_id, 'math', grade)

        demographics_generated = {}
        grade_dict = student_info_dict[grade]
        grade_total = 0
        for perf_lvl in grade_dict:
            perf_lvl_student_list = grade_dict[perf_lvl]
            grade_total += len(perf_lvl_student_list)
            for student_info in perf_lvl_student_list:
                student_demographics = student_info.getDemoOfStudent()

                ethnicities = student_info.getDemoOfStudent('dmg_eth')
                skip_eths = False
                if ('dmg_eth_2mr' in student_demographics or len(ethnicities) > 2) and 'dmg_eth_hsp' not in student_demographics:
                    # init 2 or more
                    if not demographics_generated.get('dmg_eth_2mr'):
                        demographics_generated['dmg_eth_2mr'] = [0, 0, 0, 0, 0]
                    demographics_generated['dmg_eth_2mr'][perf_lvl] += 1

                    skip_eths = True

                for demo_name in student_demographics:
                    if 'eth' in demo_name and skip_eths:
                        continue
                    if not demographics_generated.get(demo_name):
                        demographics_generated[demo_name] = [0, 0, 0, 0, 0]
                    demographics_generated[demo_name][perf_lvl] += 1

        print_grade_demographics(demographics_generated, grade, grade_total, grade_demo_percentages)


def print_grade_demographics(demographics_dict, grade, grade_total, grade_demo_percentages):
    '''
    '''
    print()
    print('Grade', grade, 'Total Students in grade', grade_total)
    print()
    print('name,total,level1,level2,level3,level4')
    sorted_names = sorted(list(demographics_dict.keys()))
    for demo_name in sorted_names:
        demo_list = demographics_dict[demo_name]
        demo_list[0] = sum(demo_list[1:])
        out_string = '%s,%s,%s,%s,%s,%s,' % (demo_name, demo_list[0], demo_list[1], demo_list[2], demo_list[3], demo_list[4])
        demo_percents = grade_demo_percentages[demo_name]
        out_string += ',%s,%s,%s,%s,%s' % (demo_percents[1], demo_percents[2], demo_percents[3], demo_percents[4], demo_percents[5])
        print(out_string)

    print()
