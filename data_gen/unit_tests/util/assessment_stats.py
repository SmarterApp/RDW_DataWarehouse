"""
TODO: enter description

@author: mjacob
@date: 140321
"""
from sbac_data_generation.util.assessment_stats import RandomLevelByDemographics, Properties, GradeLevels
from sbac_data_generation.util.assessment_stats import DemographicLevels, Stats
from nose.tools import assert_equal
from general.util.weighted_choice import weighted_choice
from collections import defaultdict, Counter

def gen_random_entity(demographics):
    return {demo_name: weighted_choice(distribution)
            for demo_name, distribution in demographics.items()}


def test_random_level():
    """

    """
    demographics = Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 0.0},
    )

    level_breakdowns = GradeLevels((14.0, 30.0, 49.0, 7.0),
            dmg_prg_504=DemographicLevels(
                {True: Stats(45.0, 37.0, 17.0, 1.0),
                 False: Stats(11.304347826086957, 29.391304347826086, 51.78260869565217, 7.521739130434782)}
            ),
            dmg_prg_tt1=DemographicLevels(
                {True: Stats(20.0, 38.0, 39.0, 3.0),
                 False: Stats(6.363636363636363, 19.818181818181817, 61.72727272727273, 12.090909090909092)}
            ),
            dmg_prg_iep=DemographicLevels(
                {True: Stats(45.0, 37.0, 17.0, 1.0),
                 False: Stats(8.529411764705882, 28.764705882352942, 54.64705882352941, 8.058823529411764)}
            ),
            dmg_prg_lep=DemographicLevels(
                {True: Stats(38.0, 43.0, 19.0, 0.0),
                 False: Stats(11.626373626373626, 28.714285714285715, 51.967032967032964, 7.6923076923076925)}
            ),
            gender=DemographicLevels(
                female=Stats(11.0, 29.0, 52.0, 8.0),
                male=Stats(16.0, 33.0, 46.0, 5.0),
                not_stated=Stats(9.0, 30.0, 51.0, 10.0),
            ),
            race=DemographicLevels(
                dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                dmg_eth_pcf=Stats(0.0, 0.0, 0.0, 0.0),
                dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0),
            ),
        )

    level_generator = RandomLevelByDemographics(demographics, level_breakdowns)

    for _ in range(10000):
        entity = gen_random_entity(demographics)
        level = level_generator.random_level(entity)
