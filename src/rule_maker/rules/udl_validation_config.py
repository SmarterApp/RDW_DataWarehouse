#@PydevCodeAnalysisIgnore
from rule_maker.rules import transformations as t
from rule_maker.rules.rule_keys import *
from rule_maker.rules import validations as v
BY_COLUMN = 'by_column'
BY_RULE = 'by_row'


# UDL config file using our notation system

validations = {
    'STG_SBAC_ASMT_OUTCOME': {
        BY_COLUMN: {
            'batch_id':[],
            'src_file_rec_num':[],
            'guid_asmt':[],
            'guid_asmt_location':[IsGoodGUID, {IsUniqueWithin: ['name_asmt_location']}],
            'name_asmt_location': IsNotNull,
            'grade_asmt':[IsNotNull, {IsInList:[3,4,5,6,7,8,11]}],
            'name_state':[],
            'code_state':[],
            'guid_district':[],
            'name_district':[],
            'guid_school':[],
            'name_school':[],
            'type_school':[],
            'guid_student':[],
            'name_student_first':[],
            'name_student_middle':[],
            'name_student_last':[],
            'address_student_line1':[],
            'address_student_line2':[],
            'address_student_city':[],
            'address_student_zip':[],
            'gender_student':[],
            'email_student':[],
            'dob_student':[],
            'grade_enrolled':[],
            'date_assessed':[],
            'score_asmt':[],
            'score_asmt_min':[],
            'score_asmt_max':[],
            'score_perf_level':[],
            'score_claim_1':[],
            'score_claim_1_min':[],
            'score_claim_1_max':[],
            'score_claim_2':[],
            'score_claim_2_min':[],
            'score_claim_2_max':[],
            'score_claim_3':[],
            'score_claim_3_min':[],
            'score_claim_3_max':[],
            'score_claim_4':[],
            'score_claim_4_min':[],
            'score_claim_4_max':[],
            'guid_staff':[],
            'name_staff_first':[],
            'name_staff_middle':[],
            'name_staff_last':[],
            'type_staff':[],
            'created_date':[]
        },
        BY_RULE: {

        }
    },
    'STG_SBAC_ASMT': {
        BY_COLUMN: {

              'guid_asmt'           : [ IsNotNull, IsGoodGUID ],
              'type'                : { IsInList : ['SUMMATIVE', 'INTERIM'] },
              'period'              : [],
              'year'                : { HasMaxLength : 4 },
              'version'             : { HasMaxLength : 2 },
              'subject'             : { IsInList : ['MATH', 'ELA'],
              'score_overall_min'   : [ IsNumber, { IsLessThan : '{score_overall_max}' } ],
              'score_overall_max'   : [ IsNumber, { IsMoreThan : '{score_overall_min}' } ],
              'name_claim_1'        : IsText,
              'score_claim_1_min'   : [ IsNumber, { IsLessThan : '{score_claim_1_max}' } ],
              'score_claim_1_max'   : [ IsNumber, { IsMoreThan : '{score_claim_1_min}' } ],
              'score_claim_1_weight': IsNumber,
              'name_claim_2'        : IsText,
              'score_claim_2_min'   : [ IsNumber, { IsLessThan : '{score_claim_2_max}' }],
              'score_claim_2_max'   : [ IsNumber, { IsMoreThan : '{score_claim_2_min}' } ],
              'score_claim_2_weight': IsNumber,
              'name_claim_3'        : IsText,
              'score_claim_3_min'   : [ IsNumber, { IsLessThan : '{score_claim_3_max}' }],
              'score_claim_3_max'   : [ IsNumber, { IsMoreThan : '{score_claim_3_min}' } ],
              'score_claim_3_weight': IsNumber,
              'name_claim_4'        : IsText,
              'score_claim_4_min'   : [ IsNumber, { IsLessThan : '{score_claim_4_max}' }],
              'score_claim_4_max'   : [ IsNumber, { IsMoreThan : '{score_claim_4_min}' } ],
              'score_claim_4_weight': IsNumber,
              'name_perf_lvl_1'     : IsText,
              'name_perf_lvl_2'     : IsText,
              'name_perf_lvl_3'     : IsText,
              'name_perf_lvl_4'     : IsText,
              'name_perf_lvl_5'     : IsText,
              'score_cut_point_1'   : [ IsNumber, {IsLessThan: '{score_cut_point_2}'} , {IsInRange: [1200,2400] } ],
              'score_cut_point_2'   : [ IsNumber, {IsLessThan: '{score_cut_point_3}'} , {IsInRange: [1200,2400] } ],
              'score_cut_point_3'   : [ IsNumber, {IsLessThan: '{score_cut_point_4}'} , {IsInRange: [1200,2400] } ],
              'score_cut_point_4'   : [ IsNumber, {IsMoreThan: '{score_cut_point_3}'} , {IsInRange: [1200,2400] } ],

        },
        t.BY_RULE: {
                    [ {NAME:'assert_SumWeight'}, {ASSERT: '{score_claim_1_weight} + {score_claim_2_weight}  + {score_claim_3_weight} +  {score_claim_4_weight} = 1.0' } ]
        }
     }
   }
 }
