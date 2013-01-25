"""
Enumeration classes for business logic.

It's common to need to store a limited number of a certain business logic item,
such as the possible applications or reports. Those can be stored here, along
with the properties that describe the items.

These are mostly in alphabetical order, except when they must reference another
enum that comes after it alphabetically.
"""


NO_FILTER_CODE = '-1'
NOT_APPLICABLE_CODE = '-2'
NOT_APPLICABLE_ABBREV = 'N/A'
NOT_APPLICABLE_NAME = 'Not Applicable'
ALL_VALUES_CODE = '-3'
ALL_VALUES_ABBREV = 'All'
ALL_VALUES_NAME = 'All'
SPECIAL_CODES = [NO_FILTER_CODE, NOT_APPLICABLE_CODE, ALL_VALUES_CODE]


class _Enum(object):
    def __init__(self, d, lookup_keys=[]):
        # make sure we can get the key back too if all we know is something else
        for key, val_dict in d.items():
            val_dict['key'] = key
        self._d = d
        self._lookup_keys = lookup_keys
        for key in d:
            self.__dict__[key] = d[key]
        for lookup_key in lookup_keys + ['code', 'name']:
            def make_lookup_f(l_key):
                def lookup_f(self, key):
                    return self._get_by_key(l_key, key)
                return lookup_f
            lookup_f = make_lookup_f(lookup_key)
            lookup_f.__name__ = 'get_by_' + lookup_key
            setattr(self.__class__, lookup_f.__name__, lookup_f)

    def get(self, item_id):
        return self._d.get(item_id)

    def all(self):
        values = [self._d[key] for key in self._d]
        if 'order' in values[0]:
            values.sort(key=lambda value: value['order'])
        return values

    def _get_by_key(self, key, value):
        for item in self._d:
            if self._d[item][key].lower() == value.lower():
                return self._d[item]
        return None

    def keys(self):
        return self._d.keys()

    def __contains__(self, v):
        return v in self._d


Assessment = _Enum({
    'CIRCLE': {
        'code': 'CIRCLE',
        'name': 'mCLASS:CIRCLE',
        'urlpath': 'CIRCLE',
        'student_url_template': '/wgen/circle/StudentSummary.do',
        'dynamic_url_params': {
            'studentSid': 'student_sid',
            'classeSid': 'classe',
            'instSid': 'school'
        }
    },
    'CIRCLEMath': {
        'code': '8m',
        'name': 'mCLASS:CIRCLE-Math',
        'urlpath': None,
        'student_url_template': '/wgen/circle/StudentSummary.do',
        'dynamic_url_params': {
            'studentSid': 'student_sid',
            'classeSid': 'classe',
            'instSid': 'school'
        }
    },
    'CIRCLELiteracy': {
        'code': '8l',
        'name': 'mCLASS:CIRCLE-Literacy',
        'urlpath': None,
        'student_url_template': '/wgen/circle/StudentSummary.do',
        'dynamic_url_params': {
            'studentSid': 'student_sid',
            'classeSid': 'classe',
            'instSid': 'school'
        }
    },
    'Reading3D': {
        'code': '3D',
        'name': 'mCLASS:Reading 3D',
        'urlpath': '3D',
        'student_url_template': '/dnext/studentSummary',
        'dynamic_url_params': {
            'eternalStudentSid': 'eternal_student_sid',
            'classe': 'classe'
        }
    },
    'DIBELS': {
        'code': '7',
        'name': 'mCLASS:DIBELS',
        'urlpath': 'DIBELS',
        'student_url_template': '/wgen/d2/StudentOverview.do',
        'dynamic_url_params': {
            'eternalStudentSid': 'eternal_student_sid',
            'selectedClasseSid': 'classe',
            'selectedInstSid': 'school'
        }
    },
    'Math': {
        'code': '22',
        'name': 'mCLASS:Math',
        'urlpath': 'Math',
        'student_url_template': '/wgen/mathcbm/StudentSummary.do',
        'dynamic_url_params': {
            'eternalStudentSid': 'eternal_student_sid',
            'classeSid': 'classe',
            'schoolSid': 'school',
            'periodSid': ''
        },
        'static_url_params': {
            'periodSid': ''
        }
    },
    'BurstReadingELI': {
        'code': '28',
        'name': 'Burst:Reading ELI',
        'urlpath': 'BurstReadingELI',
        'student_url_template': '/burstAssessment/studentSummary',
        'dynamic_url_params': {
            'eternalStudentSid': 'eternal_student_sid',
            'classe': 'classe',
        }
    },
    'TPRI': {
        'code': '5',
        'name': 'mCLASS:TPRI',
        'urlpath': 'TPRI',
        'student_url_template': '/wgen/tpri/LoadTpriStudentSummary.do',
        'dynamic_url_params': {
            'ppkEternalStudentSid': 'eternal_student_sid',
            'ppkStudentSid': 'student_sid',
            'ppkClasseSid': 'classe',
            'ppkInstSid': 'school',
        },
        'static_url_params': {
            'ppkDefaultVersionSid': '7'
        }
    },
    'Reading3DSpanish': {
        'code': '3Ds',
        'name': 'mCLASS:Reading 3D Spanish',
        'urlpath': '3Ds',
        'student_url_template': '/r3d2/spa/StudentSummary.do',
        'dynamic_url_params': {
            'currentStudent': 'eternal_student_sid',
            'currentClass': 'classe',
            'currentSchool': 'school'
        }
    },
    'IDEL': {
        'code': '11',
        'name': 'mCLASS:IDEL',
        'urlpath': 'IDEL',
        'student_url_template': '/wgen/idel2/StudentOverview.do',
        'dynamic_url_params': {
            'eternalStudentSid': 'eternal_student_sid',
            'selectedClasseSid': 'classe',
            'selectedInstSid': 'school',
        }
    },
    'TejasLEE': {
        'code': '9',
        'name': 'mCLASS:Tejas LEE',
        'urlpath': 'TejasLEE',
        'student_url_template': '/wgen/tpri/LoadTpriStudentSummary.do',
        'dynamic_url_params': {
            'ppkDefaultVersionSid': '8',
            'ppkEternalStudentSid': 'eternal_student_sid',
            'ppkStudentSid': 'student_sid',
            'ppkClasseSid': 'classe',
            'ppkInstSid': 'school',
        },
        'static_url_params': {
            'ppkDefaultVersionSid': '8'
        }
    },
    'TRC': {
        'code': '706',
        'name': 'TRC',
        'urlpath': 'TRC',
        'student_url_template': '/r3d2/eng/StudentSummary.do',
        'dynamic_url_params': {
            'currentStudent': 'eternal_student_sid',
            'currentClass': 'classe',
            'currentSchool': 'school'
        }
    },
    'TRCSpanish': {
        'code': '706s',
        'name': 'TRC Spanish',
        'urlpath': 'TRCs',
        'student_url_template': '/r3d2/spa/StudentSummary.do',
        'dynamic_url_params': {
            'currentStudent': 'eternal_student_sid',
            'currentClass': 'classe',
            'currentSchool': 'school'
        }
    },
    'Beacon': {
        'code': '30',
        'name': 'mCLASS Beacon',
        'urlpath': None,
        'student_url_template': None
    }
}, lookup_keys=['urlpath'])

Version = _Enum({
    "DNext": {
        "assmt_code": "7",
        "assmt_name": "mCLASS:DIBELS",
        "code": "32",
        "name": "DIBELS Next",
        "rank": 0,
        'student_url_template': '/dnext/studentSummary',
        'dynamic_url_params': {
            'eternalStudentSid': 'eternal_student_sid',
            'classe': 'classe'
        }
    },
    "CIRCLE": {
        "assmt_code": "CIRCLE",
        "assmt_name": "mCLASS:CIRCLE",
        "code": "1",
        "name": "CIRCLE",
        "rank": 0
    }
})

AttributeCategoryType = _Enum({
    'NA': {
        'code': NOT_APPLICABLE_CODE,
        'name': NOT_APPLICABLE_NAME
    },
    'Student': {
        'code': '1',
        'name': 'Student'
    },
    'Enrollment': {
        'code': '2',
        'name': 'Enrollment'
    },
    'AssessedInAllPeriods': {
        'code': '3',
        'name': 'Assessed in All Periods'
    }
})


AttributeCategory = _Enum({
    'Gender': {'code': 'GENDER', 'name': 'Gender', 'code_column': 'gender_code', 'name_column': 'gender_name', 'type': AttributeCategoryType.get('Student')},
    'AssessedInAllPeriods': {'code': 'ASSESSED_IN_ALL_PERIODS', 'name': 'Assessed in All Periods', 'code_column': '', 'name_column': '', 'type': AttributeCategoryType.get('AssessedInAllPeriods')},
    'Section504': {'code': 'SECTION_504', 'name': 'Section 504', 'code_column': 's504_status_code', 'name_column': 's504_status_name', 'type': AttributeCategoryType.get('Enrollment')},
    'ELLStatus': {'code': 'ELL_STATUS', 'name': 'ELL Status', 'code_column': 'ell_status_code', 'name_column': 'ell_status_name', 'type': AttributeCategoryType.get('Enrollment')},
    'Race': {'code': 'ETHNICITY', 'name': 'Race', 'code_column': 'ethnicity_code', 'name_column': 'ethnicity_name', 'type': AttributeCategoryType.get('Enrollment')},
    'HomeLanguage': {'code': 'HOME_LANGUAGE', 'name': 'Home Language', 'code_column': 'home_lang_code', 'name_column': 'home_lang_name', 'type': AttributeCategoryType.get('Enrollment')},
    'Disability': {'code': 'DISABILITY', 'name': 'Disability', 'code_column': 'disability_status_code', 'name_column': 'disability_status_name', 'type': AttributeCategoryType.get('Enrollment')},
    'SpecificDisability': {'code': 'SPECIFIC_DISABILITY', 'name': 'Specific Disability', 'code_column': 'specific_disability_code', 'name_column': 'specific_disability_name', 'type': AttributeCategoryType.get('Enrollment')},
    'HousingStatus': {'code': 'HOUSING_STATUS', 'name': 'Housing Status', 'code_column': 'housing_status_code', 'name_column': 'housing_status_name', 'type': AttributeCategoryType.get('Enrollment')},
    'MealStatus': {'code': 'MEAL_STATUS', 'name': 'Meal Status', 'code_column': 'meal_status_code', 'name_column': 'meal_status_name', 'type': AttributeCategoryType.get('Enrollment')},
    'EconDisadv': {'code': 'ECON_DISADV', 'name': 'Economically Disadvantaged', 'code_column': 'econ_disadvantage_code', 'name_column': 'econ_disadvantage_name', 'type': AttributeCategoryType.get('Enrollment')},
    'Title1': {'code': 'TITLE_1_STATUS', 'name': 'Title 1', 'code_column': 'title_1_status_code', 'name_column': 'title_1_status_name', 'type': AttributeCategoryType.get('Enrollment')},
    'Migrant': {'code': 'MIGRANT_STATUS', 'name': 'Migrant', 'code_column': 'migrant_status_code', 'name_column': 'migrant_status_name', 'type': AttributeCategoryType.get('Enrollment')},
    'EnglishProf': {'code': 'ENGLISH_PROF', 'name': 'English Proficiency', 'code_column': 'english_prof_code', 'name_column': 'english_prof_name', 'type': AttributeCategoryType.get('Enrollment')},
    'SpecialEd': {'code': 'SPED_ENVIRON', 'name': 'Special Ed.', 'code_column': 'sped_environ_code', 'name_column': 'sped_environ_name', 'type': AttributeCategoryType.get('Enrollment')},
    'AltAssmt': {'code': 'ALT_ASSMT', 'name': 'Alternate Assessment', 'code_column': 'alt_assmt_code', 'name_column': 'alt_assmt_name', 'type': AttributeCategoryType.get('Enrollment')},
    'ClassedUnclassed': {'code': 'CLASSED/UNCLASSED', 'name': 'Classed/Unclassed', 'code_column': 'is_classed_code', 'name_column': 'is_classed_name', 'type': AttributeCategoryType.get('Enrollment')}
})


BarLength = _Enum({
    'Percentage': {
        'code': '1',
        'name': 'Percentage',
        'order': 1
    },
    'HeadCount': {
        'code': '2',
        'name': 'Head Count',
        'order': 2
    }
})


GrainType = _Enum({
    'Institution': {
        'code': '1',
        'name': 'Institution'
    },
    'Grade': {
        'code': '2',
        'name': 'Grade'
    },
    'Attribute': {
        'code': '3',
        'name': 'Attribute'
    },
    'Week': {
        'code': '4',
        'name': 'Week'
    }
})


Grain = _Enum({
    'GroupOfState': {
        'code': '0',
        'name': 'GroupOfState',
        'order': 0,
        'inst_hierarchy_order': 7,
        'drillup_grain_code': '1',
        'drilldown_grain_code': '4',
        'parameter_name': 'state_groups',
        'type': GrainType.Institution
    },

    'State': {
        'code': '1',
        'name': 'State',
        'order': 1,
        'inst_hierarchy_order': 6,
        'drillup_grain_code': '1',
        'drilldown_grain_code': '2',
        'parameter_name': 'state',
        'type': GrainType.Institution
    },

    'District': {
        'code': '2',
        'name': 'District',
        'order': 2,
        'inst_hierarchy_order': 5,
        'drillup_grain_code': '1',
        'drilldown_grain_code': '4',
        'parameter_name': 'school_groups',
        'type': GrainType.Institution
    },

    'School': {
        'code': '4',
        'name': 'School',
        'order': 4,
        'inst_hierarchy_order': 4,
        'drillup_grain_code': '2',
        'drilldown_grain_code': '5',
        'parameter_name': 'schools',
        'type': GrainType.Institution
    },
    'Teacher': {
        'code': '5',
        'name': 'Teacher',
        'order': 5,
        'inst_hierarchy_order': 3,
        'drillup_grain_code': '4',
        'drilldown_grain_code': '6',
        'parameter_name': 'teachers',
        'type': GrainType.Institution
    },
    'Section': {
        'code': '6',
        'name': 'Class',
        'order': 6,
        'inst_hierarchy_order': 2,
        'drillup_grain_code': '5',
        'drilldown_grain_code': '7',
        'parameter_name': 'courses',
        'type': GrainType.Institution
    },
    'Student': {
        'code': '7',
        'name': 'Student',
        'order': 7,
        'inst_hierarchy_order': 1,
        'drillup_grain_code': '6',
        'type': GrainType.Institution
    },
    'Grade': {
        'code': '8',
        'name': 'Grade',
        'order': 8,
        'inst_hierarchy_order': None,
        'parameter_name': 'grades',
        'type': GrainType.Grade
    },
    'Week': {
        'code': '9',
        'name': 'By Week',
        'order': 9,
        'inst_hierarchy_order': None,
        'parameter_name': 'account',
        'type': GrainType.Week
    },
    'Race': {
        'code': 'ETHNICITY',
        'name': 'Race',
        'order': 10,
        'inst_hierarchy_order': None,
        'parameter_name': 'Race',
        'type': GrainType.Attribute
    },
    'Gender': {
        'code': 'GENDER',
        'name': 'Gender',
        'order': 11,
        'inst_hierarchy_order': None,
        'parameter_name': 'Gender',
        'type': GrainType.Attribute
    },
    'Section504': {
        'code': 'SECTION_504',
        'name': 'Section 504',
        'order': 12,
        'inst_hierarchy_order': None,
        'parameter_name': 'Section504',
        'type': GrainType.Attribute
    },
    'ELLStatus': {
        'code': 'ELL_STATUS',
        'name': 'ELL Status',
        'order': 13,
        'inst_hierarchy_order': None,
        'parameter_name': 'ELLStatus',
        'type': GrainType.Attribute
    },
    'HomeLanguage': {
        'code': 'HOME_LANGUAGE',
        'name': 'Home Language',
        'order': 14,
        'inst_hierarchy_order': None,
        'parameter_name': 'HomeLanguage',
        'type': GrainType.Attribute
    },
    'Disability': {
        'code': 'DISABILITY',
        'name': 'Disability',
        'order': 15,
        'inst_hierarchy_order': None,
        'parameter_name': 'Disability',
        'type': GrainType.Attribute
    },
    'SpecificDisability': {
        'code': 'SPECIFIC_DISABILITY',
        'name': 'Specific Disability',
        'order': 16,
        'inst_hierarchy_order': None,
        'parameter_name': 'SpecificDisability',
        'type': GrainType.Attribute
    },
    'HousingStatus': {
        'code': 'HOUSING_STATUS',
        'name': 'Housing Status',
        'order': 17,
        'inst_hierarchy_order': None,
        'parameter_name': 'HousingStatus',
        'type': GrainType.Attribute
    },
    'MealStatus': {
        'code': 'MEAL_STATUS',
        'name': 'Meal Status',
        'order': 18,
        'inst_hierarchy_order': None,
        'parameter_name': 'MealStatus',
        'type': GrainType.Attribute
    },
    'EconDisadv': {
        'code': 'ECON_DISADV',
        'name': 'Economically Disadvantaged',
        'order': 19,
        'inst_hierarchy_order': None,
        'parameter_name': 'EconDisadv',
        'type': GrainType.Attribute
    },
    'Title1': {
        'code': 'TITLE_1_STATUS',
        'name': 'Title 1',
        'order': 20,
        'inst_hierarchy_order': None,
        'parameter_name': 'Title1',
        'type': GrainType.Attribute
    },
    'Migrant': {
        'code': 'MIGRANT_STATUS',
        'name': 'Migrant',
        'order': 21,
        'inst_hierarchy_order': None,
        'parameter_name': 'Migrant',
        'type': GrainType.Attribute
    },
    'EnglishProf': {
        'code': 'ENGLISH_PROF',
        'name': 'English Proficiency',
        'order': 22,
        'inst_hierarchy_order': None,
        'parameter_name': 'EnglishProf',
        'type': GrainType.Attribute
    },
    'SpecialEd': {
        'code': 'SPED_ENVIRON',
        'name': 'Special Ed.',
        'order': 23,
        'inst_hierarchy_order': None,
        'parameter_name': 'SpecialEd',
        'type': GrainType.Attribute
    },
    'AltAssmt': {
        'code': 'ALT_ASSMT',
        'name': 'Alternate Assessment',
        'order': 24,
        'inst_hierarchy_order': None,
        'parameter_name': 'AltAssmt',
        'type': GrainType.Attribute
    },
    'ClassedUnclassed': {
        'code': 'CLASSED/UNCLASSED',
        'name': 'Classed/Unclassed',
        'order': 25,
        'inst_hierarchy_order': None,
        'parameter_name': 'ClassedUnclassed',
        'type': GrainType.Attribute
    }
})


InstitutionType = _Enum({
    'School': {
        'code': '1',
        'name': 'School'
    },
    'District': {
        'code': '2',
        'name': 'District'
    },
    'Muni': {
        'code': '3',
        'name': 'Muni'
    }
})


GradeDividers = _Enum({
    'Off': {
        'code': '0',
        'name': 'Disabled',
        'boolean': False,
        'order': 1
    },
    'On': {
        'code': '1',
        'name': 'Enabled',
        'boolean': True,
        'order': 2
    }
})


PerformanceMeasurement = _Enum({
    'CircleAge': {
        'code': 'CIRCLE_AGE',
        'name': 'Value',
        'aggregate_name': 'Circle Age',
        'outcome_code': 'AGE',
        'code_column': 'outcome_string_code',
        'outcome_column': 'outcome_string',
        'show_on_reports': True
    },
    'CircleLanguage': {
        'code': 'LANG',
        'name': 'Value',
        'aggregate_name': 'Circle Language',
        'outcome_code': 'LANG',
        'code_column': 'outcome_string_code',
        'outcome_column': 'outcome_string',
        'show_on_reports': True
    },
    'PerformanceLevel': {
        'code': '1',
        'name': 'Levels',
        'aggregate_name': 'Levels',
        'outcome_code': 'performance_level',
        'code_column': None,
        'outcome_column': None,
        'show_on_reports': True
    },
    'RawScore': {
        'code': '3',
        'name': 'Raw Score',
        'aggregate_name': 'Mean Score [Raw]',
        'outcome_code': 'RAWSCORE',
        'code_column': 'outcome_int_code',
        'outcome_column': 'outcome_int',
        'show_on_reports': True
    },
    'Score': {
        'code': '4',
        'name': 'Score',
        'aggregate_name': 'Mean Score',
        'outcome_code': 'SCORE',
        'code_column': 'outcome_int_code',
        'outcome_column': 'outcome_int',
        'show_on_reports': True
    },
    'StoryRead': {
        'code': '21',
        'name': 'Story Read',
        'aggregate_name': None,
        'outcome_code': 'STORYREAD',
        'code_column': 'outcome_string_code',
        'outcome_column': 'outcome_string',
        'show_on_reports': False
    },
    'StoryNumber': {
        'code': '22',
        'name': 'Story Number',
        'aggregate_name': None,
        'outcome_code': 'STORYNUM',
        'code_column': 'outcome_int_code',
        'outcome_column': 'outcome_int',
        'show_on_reports': False
    }
}, lookup_keys=['outcome_code'])


RosterOption = _Enum({
    'OnTestDay': {'code': '2', 'name': 'On Test Day'},
    'Now': {'code': '3', 'name': 'Now*'}
})


SchoolGroupType = _Enum({
    'District': {
        'code': '3',
        'name': 'Districts'
    },
})


Scope = _Enum({

    'GroupOfState': {
        'code': '0',
        'name': 'GroupOfState',
        'order': 0,
        'drillup_scope_code': '1',
        'drilldown_scope_code': '4',
        'inst_hierarchy_order': 7
    },

    'State': {
        'code': '1',
        'name': 'State',
        'order': 1,
        'drillup_scope_code': '1',
        'drilldown_scope_code': '2',
        'inst_hierarchy_order': 6
    },

    'District': {
        'code': '2',
        'name': 'District',
        'order': 2,
        'drillup_scope_code': '1',
        'drilldown_scope_code': '4',
        'inst_hierarchy_order': 5
    },
    'School': {
        'code': '4',
        'name': 'School',
        'order': 4,
        'drillup_scope_code': '3',
        'drilldown_scope_code': '5',
        'inst_hierarchy_order': 4
    },
    'Teacher': {
        'code': '5',
        'name': 'Teacher',
        'order': 5,
        'drillup_scope_code': '4',
        'drilldown_scope_code': '6',
        'inst_hierarchy_order': 3
    },
    'Section': {
        'code': '6',
        'name': 'Class',
        'order': 6,
        'drillup_scope_code': '5',
        'drilldown_scope_code': '7',
        'inst_hierarchy_order': 2
    },
    #'Student': {
    #    'code': '7',
    #    'name': 'Student',
    #    'order': 7,
    #    'drillup_scope_code': '6',
    #    'drilldown_scope_code': '7',
    #    'inst_hierarchy_order': 1
    #}
})


ReferencePoint = _Enum({
    'GroupOfState': {
        'code': '0',
        'name': 'GroupOfState',
        'order': 1,
        'scope': Scope.GroupOfState,
        'grain': Grain.GroupOfState
    },
    'State': {
        'code': '1',
        'name': 'Account',
        'order': 2,
        'scope': Scope.GroupOfState,
        'grain': Grain.State
    },
    'District': {
        'code': '2',
        'name': 'District',
        'order': 3,
        'scope': Scope.District,
        'grain': Grain.District
    },
    'School': {
        'code': '4',
        'name': 'School',
        'order': 5,
        'scope': Scope.School,
        'grain': Grain.School
    },
    'Teacher': {
        'code': '5',
        'name': 'Teacher',
        'order': 6,
        'scope': Scope.Teacher,
        'grain': Grain.Teacher
    },
    'Section': {
        'code': '6',
        'name': 'Section',
        'order': 7,
        'scope': Scope.Section,
        'grain': Grain.Section
    },
    'AggregatedTotal': {
        'code': '7',
        'name': 'Aggregated Total',
        'order': 8,
        'scope': None,
        'grain': None
    }
}, lookup_keys=['scope'])


Report = _Enum({
    'ComparingPopulations': {
        'code': '1',
        'name': 'Comparing Populations'
    },
    'StudentSummary': {
        'code': '100',
        'name': 'Student Summary'
    },
    'DDSExport': {
        'code': '101',
        'name': 'DIBELS Data System Export'
    }
})


Tag = _Enum({
    'Beacon': {
        'code': 'mCLASSBeacon',
        'name': 'mCLASS Beacon',
        'assmt_code': '30',
        'order': 1
    },
    'Reading3D': {
        'code': 'mCLASS:Reading3D',
        'name': 'mCLASS:Reading 3D DIBELS Next',
        'assmt_code': '3D',
        'order': 2
    },
    'DIBELS': {
        'code': 'mCLASS:DIBELS',
        'name': 'mCLASS:DIBELS Next',
        'assmt_code': '7',
        'order': 3
    },
    'Math': {
        'code': 'mCLASS:Math',
        'name': 'mCLASS:Math',
        'assmt_code': '22',
        'order': 4
    },
    'BurstReadingELI': {
        'code': 'Burst:ReadingELI',
        'name': 'Burst:Reading ELI',
        'assmt_code': '28',
        'order': 5
    },
    'TPRI': {
        'code': 'mCLASS:TPRI',
        'name': 'mCLASS:TPRI',
        'assmt_code': '5',
        'order': 6
    },
    'Reading3D6': {
        'code': 'mCLASS:Reading3D6',
        'name': 'mCLASS:Reading 3D',
        'assmt_code': '3D',
        'order': 7
    },
    'DIBELS6': {
        'code': 'mCLASS:DIBELS6',
        'name': 'mCLASS:DIBELS',
        'assmt_code': '7',
        'order': 8
    },
    'Reading3DSpanish': {
        'code': 'mCLASS:Reading3DSpanish',
        'name': 'mCLASS:Reading 3D Spanish',
        'assmt_code': '3Ds',
        'order': 9
    },
    'IDEL': {
        'code': 'mCLASS:IDEL',
        'name': 'mCLASS:IDEL',
        'assmt_code': '11',
        'order': 10
    },
    'TejasLEE': {
        'code': 'mCLASS:TejasLEE',
        'name': 'mCLASS:Tejas LEE',
        'assmt_code': '9',
        'order': 11
    },
    'CIRCLE': {
        'code': 'mCLASS:CIRCLE',
        'name': 'mCLASS:CIRCLE',
        'assmt_code': 'CIRCLE',
        'order': 12
    }
})


UserLevel = _Enum({
    'PII': {
        'code': '1',
        'name': 'PII',
        'level': 1
    },
    'Section': {
        'code': '2',
        'name': 'Section',
        'level': 2
    },
    'Teacher': {
        'code': '3',
        'name': 'Teacher',
        'level': 3
    },
    'School': {
        'code': '4',
        'name': 'School',
        'level': 4
    },
    'District': {
        'code': '5',
        'name': 'District',
        'level': 5
    },
    'Muni': {
        'code': '6',
        'name': 'Muni',
        'level': 6
    }
})


UserRight = _Enum({
    'None': {
        'code': '1',
        'name': 'None'
    },
    'My': {
        'code': '2',
        'name': 'My'
    },
    'All': {
        'code': '3',
        'name': 'All'
    }
})


UserRole = _Enum({
    'System': {
        'code': '0',
        'name': 'System'
    },
    'Full': {
        'code': '1',
        'name': 'Full'
    },
    'Standard': {
        'code': '2',
        'name': 'Standard'
    }
})
