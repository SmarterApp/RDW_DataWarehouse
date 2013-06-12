from rule_maker.rules import transformations as t
from rule_maker.rules.rule_keys import *
from rule_maker.rules import validations as v

BY_COLUMN = 'by_column'
BY_RULE = 'by_row'

MAX = 100

# UDL config file using our notation system

validations = {
    'STG_SBAC_ASMT_OUTCOME': {
        BY_COLUMN: {
            'batch_id':[],
            'src_file_rec_num':[],
            'guid_asmt':[IsNotNull, IsGoodGUID],
            'guid_asmt_location':[IsGoodGUID, {IsUniqueWithin: ['name_asmt_location']}],
            'name_asmt_location': IsNotNull,
            'grade_asmt':[IsNotNull, {IsInList:[3,4,5,6,7,8,11]}],
            'name_state':IsNotNull,
            'code_state':[IsNotNull, {InList: [
                'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
                'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
                'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'
            ]}],
            'guid_district':[IsNotNull, IsGoodGuid],
            'name_district':[IsNotNull, {IsUniqueWithin: 'guid_district'}],
            'guid_school':[IsNotNull, IsGoodGUID],
            'name_school':IsNotNull,
            'type_school':[IsNotNull, {InList: ['High School', 'Middle School', 'Elementary School']},
                           {IsUniqueWithin: ['guid_school', 'name_school']}],
            'guid_student':[IsNotNull, IsGoodGUID],
            'name_student_first':[IsNotNull, IsSQLSafe, {HasMaxLength: MAX}],
            'name_student_middle':[IsSQLSafe, {HasMaxLength: MAX}],
            'name_student_last':[IsNotNull, IsSQLSafe, {HasMaxLength: MAX}],
            'address_student_line1':[IsNotNull, IsSQLSafe, {HasMaxLength: MAX}],
            'address_student_line2':[IsSqlSafe, {HasMaxLength: MAX}],
            'address_student_city':[IsNotNull, {HasMaxLength: MAX}],
            'address_student_zip':[IsNotNull, {HasMaxLength: MAX}],
            'gender_student':[IsNotNull, {IsInList: ['male', 'female']}],
            'email_student':[IsNotNull, IsGoodEmail, {HasMaxLength: MAX}],
            'dob_student':[IsNotNull, IsGoodDate, {IsUniqueWithin: ['guid_student', 'name_student_first', 'name_student_middle',
                                                                    'name_student_last', 'address_student_line_1',
                                                                    'address_student_line_2', 'address_student_city',
                                                                    'address_student_zip', 'gender_student', 'email_student']}],
            'grade_enrolled':{InList: [3,4,5,6,7,8,11]},
            'date_assessed': [IsNotNull, IsGoodDate],
            'score_asmt': [IsNotNull, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_asmt_min': [IsNotNull, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_asmt_max': IsNotNull,
            'score_perf_level': [IsNotNull, {InList : [1,2,3,4]}],
            'score_claim_1': [IsNumber, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_claim_1_min': [IsNumber, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_claim_1_max': IsNumber,
            'score_claim_2':[IsNumber, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_claim_2_min':[IsNumber, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_claim_2_max': IsNumber,
            'score_claim_3':[IsNumber, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_claim_3_min':[IsNumber, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_claim_3_max': IsNumber,
            'score_claim_4':[IsNumber, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_claim_4_min':[IsNumber, {IsGreaterThan: 1200}, {IsLessThan: 2400}],
            'score_claim_4_max':IsNumber,
            'guid_staff':[IsNotNull, IsGoodGUID],
            'name_staff_first':[IsNotNull, {HasMaxLength: MAX}],
            'name_staff_middle':{HasMaxLength: MAX},
            'name_staff_last':[IsNotNull, {HasMaxLength: MAX}],
            'type_staff':[IsNotNull, {IsInList: ['Teacher', 'Staff']}, {IsUniqueWithin:['guid_staff', 'name_staff_first',
                                                                                        'name_staff_middle', 'name_staff_last']}],
            'created_date':[]
        },
        BY_RULE: {

        }
    },
    'STG_SBAC_ASMT': {
        BY_COLUMN: {

              'guid_asmt': [ IsNotNull, IsGoodGUID ],
              'type': { IsInList : ['SUMMATIVE', 'INTERIM'] },
              'period': [],
              'year': { HasMaxLength : 4 },
              'version': { HasMaxLength : 2 },
              'subject': { IsInList : ['MATH', 'ELA'],
              'score_overall_min': [ IsNumber, { IsLessThan : '{score_overall_max}' } ],
              'score_overall_max': [ IsNumber, { IsMoreThan : '{score_overall_min}' } ],
              'name_claim_1': IsText,
              'score_claim_1_min': [ IsNumber, { IsLessThan : '{score_claim_1_max}' } ],
              'score_claim_1_max': [ IsNumber, { IsMoreThan : '{score_claim_1_min}' } ],
              'score_claim_1_weight': IsNumber,
              'name_claim_2': IsText,
              'score_claim_2_min': [ IsNumber, { IsLessThan : '{score_claim_2_max}' }],
              'score_claim_2_max': [ IsNumber, { IsMoreThan : '{score_claim_2_min}' } ],
              'score_claim_2_weight': IsNumber,
              'name_claim_3': IsText,
              'score_claim_3_min': [ IsNumber, { IsLessThan : '{score_claim_3_max}' }],
              'score_claim_3_max': [ IsNumber, { IsMoreThan : '{score_claim_3_min}' } ],
              'score_claim_3_weight': IsNumber,
              'name_claim_4': IsText,
              'score_claim_4_min': [ IsNumber, { IsLessThan : '{score_claim_4_max}' }],
              'score_claim_4_max': [ IsNumber, { IsMoreThan : '{score_claim_4_min}' } ],
              'score_claim_4_weight': IsNumber,
              'name_perf_lvl_1': IsText,
              'name_perf_lvl_2': IsText,
              'name_perf_lvl_3': IsText,
              'name_perf_lvl_4': IsText,
              'name_perf_lvl_5': IsText,
              'score_cut_point_1': [ IsNumber, {IsLessThan: '{score_cut_point_2}'} , {IsInRange: [1200,2400] } ],
              'score_cut_point_2': [ IsNumber, {IsLessThan: '{score_cut_point_3}'} , {IsInRange: [1200,2400] } ],
              'score_cut_point_3': [ IsNumber, {IsLessThan: '{score_cut_point_4}'} , {IsInRange: [1200,2400] } ],
              'score_cut_point_4': [ IsNumber, {IsMoreThan: '{score_cut_point_3}'} , {IsInRange: [1200,2400] } ],

        },
        t.BY_RULE: {
                    [ {NAME:'assert_SumWeight'}, {ASSERT: '{score_claim_1_weight} + {score_claim_2_weight}  + {score_claim_3_weight} +  {score_claim_4_weight} = 1.0' } ]
        }
     }
   }
 }
