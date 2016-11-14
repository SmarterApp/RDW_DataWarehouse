from DataGeneration.src.generators.generate_scores import generate_overall_scores
from DataGeneration.src.calc.claim_score_calculation import translate_scores_to_assessment_score


DMG_ETH_NST = 'dmg_eth_nst'
DMG_ETH_2MR = 'dmg_eth_2mr'


def assign_scores_for_subjects(studentinfo_list, demo_perf, cut_points, min_score, max_score, grade, subject, assessment, ebmin, ebmax, rndlo, rndhi, claim_cut_points):
    """
    Main function to assign scores to students for one subject
    @param studentinfo_list: list of StudentInfo object
    @param demo_perf: it is a dictionary. The key is demographic name, the value is a list which has 4 integers for 4 percentage numbers
     Example: demo_perf = {'dmg_eth_hsp': [13, 37, 43, 7],
                           'dmg_eth_ami': [12, 36, 43, 9],
                           'dmg_eth_asn': [3, 16, 53, 28],
                           'dmg_eth_blk': [17, 40, 37, 6],
                           'dmg_eth_pcf': [3, 16, 54, 28],
                           'dmg_eth_wht': [5, 25, 54, 16],
                           'dmg_eth_nst': [25, 25, 25, 25],
                           'dmg_eth_2mr': [25, 25, 25, 25]}
    @param cut_points: list of cut points. The first is the min score, the last is the max score. Example: cut_points = [1200, 1400, 1800, 2100, 2400]
    @param min_score: min score. Same as cut_points[0]
    @param min_score: max score. Same as cut_points[-1]
    @param grade: grade number
    @param subject: subject name
    @param assessment: assessment object. Its subject should be same as subject
    @param ebmin: error band min
    @param ebmax: error band max
    @param rndlo: random_adjustment_points_low
    @param rndhi: random_adjustment_points_high
    For ebmin, ebmax, rndlo, rndhi, they can be got from dg_types.get_error_band()
    """
    # calculate student's demo dict
    student_demo_counts = count_student_demographics(studentinfo_list)

    # generate scores
    for demo, studentinfo_subset in student_demo_counts.items():
        if demo not in list(demo_perf.keys()):
            continue
        perf = demo_perf[demo]
        total_students = len(studentinfo_subset)
        scores = generate_overall_scores(perf, cut_points, min_score, max_score, total_students)
        asmt_scores = translate_scores_to_assessment_score(scores, cut_points[1:-1], assessment, ebmin, ebmax, rndlo, rndhi, claim_cut_points)
        for i in range(len(studentinfo_subset)):
            studentinfo_subset[i].asmt_scores[assessment.asmt_guid] = asmt_scores[i]


def count_student_demographics(studentinfo_list):
    """
    This is a function to count student demographics for given list of StudentInfo object
    @param studentinfo_list: list of StudentInfo objects
    @return: a dictionary. The key is all demographics, and the value is list of StudentInfo objects
    For example: {'dmg_eth_nst': [StudentInfo1, StudentInfo2],
                  'dmg_eth_2mr': [StudentInfo3, StudentInfo4, StudentInfo5],
                  'dmg_eth_hsp': [StudentInfo6],
                  ...}
    """
    student_demo_dict = {}
    student_demo_dict.update({DMG_ETH_NST: []})
    student_demo_dict.update({DMG_ETH_2MR: []})

    for student_info in studentinfo_list:
        student_demos = student_info.getDemoOfStudent()
        # not stated
        if DMG_ETH_NST in student_demos or len(student_demos) == 0:
            student_demo_dict[DMG_ETH_NST].append(student_info)
        # two or more races
        elif DMG_ETH_2MR in student_demos:
            student_demo_dict[DMG_ETH_2MR].append(student_info)
        # only one demographic in each grouping
        else:
            for demo in student_demos:
                if demo not in student_demo_dict.keys():
                    student_demo_dict.update({demo: [student_info]})
                else:
                    student_demo_dict[demo].append(student_info)
    return student_demo_dict
