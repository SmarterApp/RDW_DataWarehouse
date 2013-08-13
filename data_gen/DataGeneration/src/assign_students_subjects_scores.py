from DataGeneration.src.helper_entities import StudentInfo
from DataGeneration.src.generate_scores import generate_overall_scores
from DataGeneration.src.claim_score_calculation import translate_scores_to_assessment_score
from DataGeneration.src.entities import Assessment
from DataGeneration.src.generate_entities import generate_assessment


DMG_ETH_NST = 'dmg_eth_nst'
DMG_ETH_2MR = 'dmg_eth_2mr'


def assign_scores_for_subjects(studentinfo_list, demo_perf, cut_points, min_score, max_score, grade, subject, assessment, ebmin, ebmax, rndlo, rndhi):
    """
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
        asmt_scores = translate_scores_to_assessment_score(scores, cut_points[1:-1], assessment, ebmin, ebmax, rndlo, rndhi)
        for i in range(len(studentinfo_subset)):
            (studentinfo_subset[i].asmt_scores)[subject] = asmt_scores[i]
    # return
    # verify
    verify_demo_scores(studentinfo_list, demo_perf, cut_points, min_score, max_score, grade, subject, assessment, ebmin, ebmax, rndlo, rndhi)


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


def verify_demo_scores(studentinfo_list, demo_perf, cut_points, min_score, max_score, grade, subject, assessment, ebmin, ebmax, rndlo, rndhi):
    student_demo_perf_dict = {}
    for studentinfo in studentinfo_list:
        student_demo = studentinfo.getDemoOfStudent()
        subject_score = studentinfo.asmt_scores[subject].overall_score
        for demo in student_demo:
            if demo.startswith('dmg_'):
                level = calcualte_perf_level(subject_score, cut_points)
                if demo in list(student_demo_perf_dict.keys()):
                    student_demo_perf_dict[demo][level - 1] += 1
                else:
                    perf_count = [0, 0, 0, 0]
                    perf_count[level - 1] = 1
                    student_demo_perf_dict.update({demo: perf_count})
    # convert to percentage
    for key, value in student_demo_perf_dict.items():
        total = sum(value)
        value = [round(v / total * 100) for v in value]
        student_demo_perf_dict[key] = value
#     print('*******\ndemo_name, calculated_perc, required_perc\n____________________________________')
#     for key, value in student_demo_perf_dict.items():
#         print(key, value, demo_perf[key])


def calcualte_perf_level(subject_score, cut_points):
    if cut_points[0] <= subject_score < cut_points[1]:
        return 1
    if cut_points[1] <= subject_score < cut_points[2]:
        return 2
    if cut_points[2] <= subject_score < cut_points[3]:
        return 3
    if cut_points[3] <= subject_score < cut_points[4]:
        return 4
    return -1


if __name__ == '__main__':
    # make student info
    studentinfo_list = []
    # 300 for 'dmg_eth_hsp'
    for i in range(300):
        studentinfo_list.append(StudentInfo(3, 'female', {'Math': 2400}, dmg_eth_hsp=True))
    for i in range(200):
        studentinfo_list.append(StudentInfo(3, 'female', {'Math': 2400}, dmg_eth_ami=True))
    for i in range(400):
        studentinfo_list.append(StudentInfo(3, 'female', {'Math': 2400}, dmg_eth_asn=True))
    for i in range(300):
        studentinfo_list.append(StudentInfo(3, 'female', {'Math': 2400}, dmg_eth_blk=True))
    for i in range(500):
        studentinfo_list.append(StudentInfo(3, 'female', {'Math': 2400}, dmg_eth_pcf=True))
    for i in range(600):
        studentinfo_list.append(StudentInfo(3, 'female', {'Math': 2400}, dmg_eth_wht=True))
    for i in range(50):
        studentinfo = StudentInfo(3, 'female', {'Math': 2400})
        studentinfo.dmg_eth_nst = True
        studentinfo_list.append(studentinfo)
    for i in range(200):
        studentinfo = StudentInfo(3, 'female', {'Math': 2400})
        studentinfo.dmg_eth_2mr = True
        studentinfo_list.append(studentinfo)

    demo_perf = {'dmg_eth_hsp': [13, 37, 43, 7],
                 'dmg_eth_ami': [12, 36, 43, 9],
                 'dmg_eth_asn': [3, 16, 53, 28],
                 'dmg_eth_blk': [17, 40, 37, 6],
                 'dmg_eth_pcf': [3, 16, 54, 28],
                 'dmg_eth_wht': [5, 25, 54, 16],
                 'dmg_eth_nst': [25, 25, 25, 25],
                 'dmg_eth_2mr': [25, 25, 25, 25]}
    cut_points = [1200, 1400, 1800, 2100, 2400]
    min_score = 1200
    max_score = 2400
    grade = 3
    subject = 'ELA'
    assessment = generate_assessment('SUMMATIVE', str(2012), 2012, subject, grade, cut_points[0], cut_points[1], cut_points[2], None, '09/01/2011', True, to_date='09/01/2012')
    ebmin = 32
    ebmax = 8
    rndlo = -10
    rndhi = 25
    assign_scores_for_subjects(studentinfo_list, demo_perf, cut_points, min_score, max_score, grade, subject, assessment, ebmin, ebmax, rndlo, rndhi)
