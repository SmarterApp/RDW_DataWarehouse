import unittest
from DataGeneration.src.utils.assign_students_subjects_scores import assign_scores_for_subjects
from DataGeneration.src.models.helper_entities import StudentInfo
from DataGeneration.src.generators.generate_entities import generate_assessment
import random
import math


class TestAssignStudentsSubjectsScores(unittest.TestCase):

    def test_assign_scores_for_subjects(self):
        gender_list = ['male', 'female']
        cut_points = [1200, 1400, 1800, 2100, 2400]
        claim_cut_points = [1600, 2000]
        min_score = cut_points[0]
        max_score = cut_points[-1]
        subject = 'ELA'
        grade = 3

        # make student info
        studentinfo_list = []
        for _i in range(300):
            studentinfo_list.append(StudentInfo(grade, random.choice(gender_list), {'Math': random.randint(min_score, max_score)}, dmg_eth_hsp=True))
        for _i in range(200):
            studentinfo_list.append(StudentInfo(grade, random.choice(gender_list), {'Math': random.randint(min_score, max_score)}, dmg_eth_ami=True))
        for _i in range(400):
            studentinfo_list.append(StudentInfo(grade, random.choice(gender_list), {'Math': random.randint(min_score, max_score)}, dmg_eth_asn=True))
        for _i in range(300):
            studentinfo_list.append(StudentInfo(grade, random.choice(gender_list), {'Math': random.randint(min_score, max_score)}, dmg_eth_blk=True))
        for _i in range(500):
            studentinfo_list.append(StudentInfo(grade, random.choice(gender_list), {'Math': random.randint(min_score, max_score)}, dmg_eth_pcf=True))
        for _i in range(600):
            studentinfo_list.append(StudentInfo(grade, random.choice(gender_list), {'Math': random.randint(min_score, max_score)}, dmg_eth_wht=True))
        for _i in range(50):
            studentinfo = StudentInfo(grade, random.choice(gender_list), {'Math': random.randint(min_score, max_score)})
            studentinfo.dmg_eth_nst = True
            studentinfo_list.append(studentinfo)
        for _i in range(200):
            studentinfo = StudentInfo(grade, random.choice(gender_list), {'Math': random.randint(min_score, max_score)})
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

        assessment = generate_assessment('SUMMATIVE', str(2012), 2012, subject, grade, cut_points[0], cut_points[1],
                                         cut_points[2], claim_cut_points[0], claim_cut_points[1], None,
                                         '09/01/2011', True, to_date='09/01/2012')
        ebmin = 32
        ebmax = 8
        rndlo = -10
        rndhi = 25
        assign_scores_for_subjects(studentinfo_list, demo_perf, cut_points, min_score, max_score, grade, subject, assessment, ebmin, ebmax, rndlo, rndhi, claim_cut_points)

        self._verify(studentinfo_list, demo_perf, cut_points, min_score, max_score, grade, subject, assessment, ebmin, ebmax, rndlo, rndhi)

    def _verify(self, studentinfo_list, demo_perf, cut_points, min_score, max_score, grade, subject, assessment, ebmin, ebmax, rndlo, rndhi):
        student_demo_perf_dict = {}
        for studentinfo in studentinfo_list:
            student_demo = studentinfo.getDemoOfStudent()
            subject_score = studentinfo.asmt_scores[assessment.asmt_guid].overall_score
            for demo in student_demo:
                if demo.startswith('dmg_'):
                    level = self._calcualte_perf_level(subject_score, cut_points)
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

        # verify
        for key, actual_value in student_demo_perf_dict.items():
            expected_value = demo_perf[key]
            self.assertEqual(len(actual_value), len(expected_value))
            diff = [math.fabs(actual_value[i] - expected_value[i]) for i in range(len(actual_value))]
            for d in diff:
                # we allow 5% difference
                self.assertTrue(d < 5)

    def _calcualte_perf_level(self, subject_score, cut_points):
        if cut_points[0] <= subject_score < cut_points[1]:
            return 1
        if cut_points[1] <= subject_score < cut_points[2]:
            return 2
        if cut_points[2] <= subject_score < cut_points[3]:
            return 3
        if cut_points[3] <= subject_score < cut_points[4]:
            return 4
        return -1
