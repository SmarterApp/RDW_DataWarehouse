"""
Configuration for the hierarchy generators.

:author: nestep
:date: February 21, 2014
"""

# District sizes : min/max/avg schools per type of district
SML_MIN = 5
SML_MAX = 2 * SML_MIN
SML_AVG = int((SML_MAX + SML_MIN) / 2)

MED_MIN = 4 * SML_MIN  # if small min =  5 then medium min = 20
MED_MAX = 4 * SML_MAX  # if small max = 10 then medium max = 40
MED_AVG = int((MED_MAX + MED_MIN) / 2)

BIG_MIN = 4 * MED_MIN  # if medium min = 20 then big min =  80
BIG_MAX = 4 * MED_MAX  # if medium max = 40 then big max = 160
BIG_AVG = int((BIG_MAX + BIG_MIN) / 2)

# School ratios
BASE_HIGH = 1
BASE_MIDL = 2
BASE_ELEM = 5
# ratios for 'average' schools
NORM_HIGH = 4 * BASE_HIGH
NORM_MIDL = 4 * BASE_MIDL
NORM_ELEM = 4 * BASE_ELEM
# ratios for 'featured' schools (good schools in good districts, poor schools in poor districts)
FEAT_HIGH = 6 * BASE_HIGH
FEAT_MIDL = 6 * BASE_MIDL
FEAT_ELEM = 6 * BASE_ELEM
# ratios for 'other' schools (poor schools in good districts, good schools in poor districts)
OTHR_HIGH = 1 * BASE_HIGH
OTHR_MIDL = 1 * BASE_MIDL
OTHR_ELEM = 1 * BASE_ELEM

VERY_NORM_HIGH = 3 * BASE_HIGH
VERY_NORM_MIDL = 3 * BASE_MIDL
VERY_NORM_ELEM = 3 * BASE_ELEM

VERY_FEAT_HIGH = 7 * BASE_HIGH
VERY_FEAT_MIDL = 7 * BASE_MIDL
VERY_FEAT_ELEM = 7 * BASE_ELEM


SCHOOL_TYPES = {'High School': {'type': 'High School',
                                'grades': [11],
                                'students': {'min': 50, 'max': 250, 'avg': 100}},
                'Middle School': {'type': 'Middle School',
                                  'grades': [6, 7, 8],
                                  'students': {'min': 25, 'max': 100, 'avg': 50}},
                'Elementary School': {'type': 'Elementary School',
                                      'grades': [3, 4, 5],
                                      'students': {'min': 10, 'max': 35, 'avg': 30}},
                'Poor High School': {'type': 'High School',
                                     'grades': [11],
                                     'students': {'min': 50, 'max': 250, 'avg': 100}, 'adjust_pld': -0.45},
                'Poor Middle School': {'type': 'Middle School',
                                       'grades': [6, 7, 8],
                                       'students': {'min': 25, 'max': 100, 'avg': 50}, 'adjust_pld': -0.5},
                'Poor Elementary School': {'type': 'Elementary School',
                                           'grades': [3, 4, 5],
                                           'students': {'min': 10, 'max': 35, 'avg': 30}, 'adjust_pld': -0.6},
                'Good High School': {'type': 'High School',
                                     'grades': [11],
                                     'students': {'min': 50, 'max': 250, 'avg': 100}, 'adjust_pld': 0.35},
                'Good Middle School': {'type': 'Middle School',
                                       'grades': [6, 7, 8],
                                       'students': {'min': 25, 'max': 100, 'avg': 50}, 'adjust_pld': 0.4},
                'Good Elementary School': {'type': 'Elementary School',
                                           'grades': [3, 4, 5],
                                           'students': {'min': 10, 'max': 35, 'avg': 30}, 'adjust_pld': 0.5},
                }

DISTRICT_TYPES = {'Big Average': {'school_counts': {'min': BIG_MIN, 'max': BIG_MAX, 'avg': BIG_AVG},  # if SML_MIN = 5 then (80, 160, 120)
                                  'school_types_and_ratios': {'High School': NORM_HIGH,
                                                              'Middle School': NORM_MIDL,
                                                              'Elementary School': NORM_ELEM}},
                  'Big Good': {'school_counts': {'min': BIG_MIN, 'max': BIG_MAX, 'avg': BIG_AVG},
                               'school_types_and_ratios': {'High School': NORM_HIGH,
                                                           'Middle School': NORM_MIDL,
                                                           'Elementary School': NORM_ELEM,
                                                           'Good High School': FEAT_HIGH,
                                                           'Good Middle School': FEAT_MIDL,
                                                           'Good Elementary School': FEAT_ELEM,
                                                           'Poor High School': OTHR_HIGH,
                                                           'Poor Middle School': OTHR_MIDL,
                                                           'Poor Elementary School': OTHR_ELEM}},
                  'Big Poor': {'school_counts': {'min': BIG_MIN, 'max': BIG_MAX, 'avg': BIG_AVG},
                               'school_types_and_ratios': {'High School': NORM_HIGH,
                                                           'Middle School': NORM_MIDL,
                                                           'Elementary School': NORM_ELEM,
                                                           'Poor High School': FEAT_HIGH,
                                                           'Poor Middle School': FEAT_MIDL,
                                                           'Poor Elementary School': FEAT_ELEM,
                                                           'Good High School': OTHR_HIGH,
                                                           'Good Middle School': OTHR_MIDL,
                                                           'Good Elementary School': OTHR_ELEM}},
                  'Medium Average': {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},  # if SML_MIN = 5 then (20, 40, 30)
                                     'school_types_and_ratios': {'High School': NORM_HIGH,
                                                                 'Middle School': NORM_MIDL,
                                                                 'Elementary School': NORM_ELEM}},
                  'Medium Good': {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
                                  'school_types_and_ratios': {'High School': NORM_HIGH,
                                                              'Middle School': NORM_MIDL,
                                                              'Elementary School': NORM_ELEM,
                                                              'Good High School': FEAT_HIGH,
                                                              'Good Middle School': FEAT_MIDL,
                                                              'Good Elementary School': FEAT_ELEM,
                                                              'Poor High School': OTHR_HIGH,
                                                              'Poor Middle School': OTHR_MIDL,
                                                              'Poor Elementary School': OTHR_ELEM}},
                  'Medium Very Good': {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
                                       'school_types_and_ratios': {'High School': VERY_NORM_HIGH,
                                                                   'Middle School': VERY_NORM_MIDL,
                                                                   'Elementary School': VERY_NORM_ELEM,
                                                                   'Good High School': VERY_FEAT_HIGH,
                                                                   'Good Middle School': VERY_FEAT_MIDL,
                                                                   'Good Elementary School': VERY_FEAT_ELEM}},
                   'Medium Very Poor': {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
                                        'school_types_and_ratios': {'High School': VERY_NORM_HIGH,
                                                                    'Middle School': VERY_NORM_MIDL,
                                                                    'Elementary School': VERY_NORM_ELEM,
                                                                    'Poor High School': VERY_FEAT_HIGH,
                                                                    'Poor Middle School': VERY_FEAT_MIDL,
                                                                    'Poor Elementary School': VERY_FEAT_ELEM}},
                  'Medium Poor': {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
                                  'school_types_and_ratios': {'High School': NORM_HIGH,
                                                              'Middle School': NORM_MIDL,
                                                              'Elementary School': NORM_ELEM,
                                                              'Poor High School': FEAT_HIGH,
                                                              'Poor Middle School': FEAT_MIDL,
                                                              'Poor Elementary School': FEAT_ELEM,
                                                              'Good High School': OTHR_HIGH,
                                                              'Good Middle School': OTHR_MIDL,
                                                              'Good Elementary School': OTHR_ELEM}},
                  'Small Average': {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},  # if SML_MIN = 5 then (5, 10, 7)
                                    'school_types_and_ratios': {'High School': NORM_HIGH,
                                                                'Middle School': NORM_MIDL,
                                                                'Elementary School': NORM_ELEM}},
                  'Small Good': {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
                                 'school_types_and_ratios': {'High School': NORM_HIGH,
                                                             'Middle School': NORM_MIDL,
                                                             'Elementary School': NORM_ELEM,
                                                             'Good High School': FEAT_HIGH,
                                                             'Good Middle School': FEAT_MIDL,
                                                             'Good Elementary School': FEAT_ELEM,
                                                             'Poor High School': OTHR_HIGH,
                                                             'Poor Middle School': OTHR_MIDL,
                                                             'Poor Elementary School': OTHR_ELEM}},
                  'Small Very Good': {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
                                      'school_types_and_ratios': {'High School': VERY_NORM_HIGH,
                                                                  'Middle School': VERY_NORM_MIDL,
                                                                  'Elementary School': VERY_NORM_ELEM,
                                                                  'Good High School': VERY_FEAT_HIGH,
                                                                  'Good Middle School': VERY_FEAT_MIDL,
                                                                  'Good Elementary School': VERY_FEAT_ELEM}},
                  'Small Very Poor': {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
                                      'school_types_and_ratios': {'High School': VERY_NORM_HIGH,
                                                                  'Middle School': VERY_NORM_MIDL,
                                                                  'Elementary School': VERY_NORM_ELEM,
                                                                  'Poor High School': VERY_FEAT_HIGH,
                                                                  'Poor Middle School': VERY_FEAT_MIDL,
                                                                  'Poor Elementary School': VERY_FEAT_ELEM}},
                  'Small Poor': {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
                                 'school_types_and_ratios': {'High School': NORM_HIGH,
                                                             'Middle School': NORM_MIDL,
                                                             'Elementary School': NORM_ELEM,
                                                             'Poor High School': FEAT_HIGH,
                                                             'Poor Middle School': FEAT_MIDL,
                                                             'Poor Elementary School': FEAT_ELEM,
                                                             'Good High School': OTHR_HIGH,
                                                             'Good Middle School': OTHR_MIDL,
                                                             'Good Elementary School': OTHR_ELEM}}
                  }

STATE_TYPES = {'typical_1': {'district_types_and_counts': {'Big Average': 1, 'Big Poor': 1, 'Big Good': 1,
                                                           'Medium Average': 2, 'Medium Poor': 1, 'Medium Good': 1,
                                                           'Medium Very Poor': 1, 'Medium Very Good': 1,
                                                           'Small Average': 10, 'Small Poor': 5, 'Small Good': 5,
                                                           'Small Very Poor': 5, 'Small Very Good': 5},
                             'subject_skip_percentages': {'Math': .01, 'ELA': .01},
                             'demographics': 'typical1'},
               'devel': {'district_types_and_counts': {'Small Average': 1, 'Small Poor': 1, 'Small Good': 1},
                         'subject_skip_percentages': {'Math': .01, 'ELA': .01},
                         'demographics': 'typical1'}
               }
