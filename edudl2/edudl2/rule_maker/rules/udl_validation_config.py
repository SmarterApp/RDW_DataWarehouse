#@PydevCodeAnalysisIgnore
from edudl2.rule_maker.rules import transformations as t
from edudl2.rule_maker.rules.rule_keys import *

BY_COLUMN = 'by_column'  # BY_COLUMN rules validate the indicated rule specific to the field it is tagged to
BY_RULE = 'by_row'  # BY_RULE rules validate assert conditions - these represent the true/correct state that must exists across multiple columns


## ------------------- Rule Scope ---------------------------------------------------------
EACH = 'each'  # (default) a rule applies to a single column and checks (in parallel) EACH row
                            # put an entry into the ERR table for each bad row
                            # (was ROW rule in old-UDL)
ALL = 'all'  # only an error if every row fails for this column (COLUMN rule in old-UDL)
                            # put ONE entry in ERR table, and only if ALL rows are bad for this column
                            # (was COL rule in old-UDL)
BOTH = 'both'  # if ALL rows are bad, then one entry in ERR table
                            # if not, then check EACH row
                            # (this magically happens in old-UDL)
## ------------------------------------------------------------------------------------------


# ----- This section represents constant values that are referred to in the below rules -----
DEFAULT_MAX_LENGTH = 256
MIN_ASMT_SCORE = 1200
MAX_ASMT_SCORE = 2400
#--------------------------------------------------------------------------------------------


# ------------------------------------ UDL Validations---------------------------------------

validations = {
    'STG_SBAC_ASMT_OUTCOME': {
        BY_COLUMN: {
            'guid_batch'            : [],
            'src_file_rec_num'      : [],
            'guid_asmt'             : [[IsNotNull] , IsGoodGUID],
            'guid_asmt_location'    : [IsGoodGUID, {IsUniqueWithin: ['name_asmt_location']}],
            'name_asmt_location'    : IsNotNull,
            'grade_asmt'            : [IsNotNull, {IsInList:[3, 4, 5, 6, 7, 8, 11]}],
            'name_state'            : [IsNotNull, {HasMaxLength: 32}],
            'code_state'            : [IsNotNull, {IsInList: [
                                                   'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
                                                   'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
                                                   'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
                                                   'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']}],
            'guid_district'         : [IsNotNull, IsGoodGUID],
            'name_district'         : [IsNotNull, {HasMaxLength: DEFAULT_MAX_LENGTH}, {IsUniqueWithin: 'guid_district'}],
            'guid_school'           : [IsNotNull, IsGoodGUID],
            'name_school'           : [IsNotNull, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'type_school'           : [IsNotNull, {IsInList: ['High School', 'Middle School', 'Elementary School']},
                                                  {IsUniqueWithin: ['guid_school', 'name_school']}],
            'guid_student'          : [IsNotNull, IsGoodGUID,
                                       {IsUniqueWithin: ['name_student_first', 'name_student_middle',
                                                         'name_student_last', 'address_student_line_1',
                                                         'address_student_line_2', 'address_student_city',
                                                         'address_student_zip', 'gender_student', 'email_student']}],
            'name_student_first'    : [IsNotNull, IsSQLSafe, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'name_student_middle'   : [IsSQLSafe, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'name_student_last'     : [IsNotNull, IsSQLSafe, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'address_student_line1' : [IsNotNull, IsSQLSafe, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'address_student_line2' : [IsSQLSafe, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'address_student_city'  : [IsNotNull, {HasMaxLength: 100}],
            'address_student_zip'   : [IsNotNull, {HasMaxLength: 5  }],
            'gender_student'        : [IsNotNull, {IsInList: ['male', 'female']}],
            'email_student'         : [IsNotNull, IsGoodEmail, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'dob_student'           : [IsNotNull, IsGoodDate],
            'grade_enrolled'        : {IsInList: [3, 4, 5, 6, 7, 8, 11]},
            'date_assessed'         : [IsNotNull, IsGoodDate],
            'score_asmt'            : [IsNotNull, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_asmt_min'        : [IsNotNull, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_asmt_max'        : IsNotNull,
            'score_perf_level'      : [IsNotNull, {IsInList : [1, 2, 3, 4]}],
            'score_claim_1'         : [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_claim_1_min'     : [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_claim_1_max'     : IsNumber,
            'score_claim_2'         : [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_claim_2_min'     : [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_claim_2_max'     : IsNumber,
            'score_claim_3'         : [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_claim_3_min'     : [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_claim_3_max'     : IsNumber,
            'score_claim_4'         : [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_claim_4_min'     : [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] }],
            'score_claim_4_max'     : IsNumber,
            'guid_staff'            : [IsNotNull, IsGoodGUID],
            'name_staff_first'      : [IsNotNull, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'name_staff_middle'     : {HasMaxLength: DEFAULT_MAX_LENGTH},
            'name_staff_last'       : [IsNotNull, {HasMaxLength: DEFAULT_MAX_LENGTH}],
            'type_staff'            : [IsNotNull, {IsInList: ['Teacher', 'Staff']},
                                       {IsUniqueWithin:['guid_staff', 'name_staff_first', 'name_staff_middle', 'name_staff_last']}],
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
              'name_perf_lvl_1'     : [IsSQLSafe, IsText],
              'name_perf_lvl_2'     : [IsSQLSafe, IsText],
              'name_perf_lvl_3'     : [IsSQLSafe, IsText],
              'name_perf_lvl_4'     : [IsSQLSafe, IsText],
              'name_perf_lvl_5'     : [IsSQLSafe, IsText],
              'score_cut_point_1'   : [ IsNumber, {IsLessThan: '{score_cut_point_2}'} , {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] } ],
              'score_cut_point_2'   : [ IsNumber, {IsLessThan: '{score_cut_point_3}'} , {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] } ],
              'score_cut_point_3'   : [ IsNumber, {IsLessThan: '{score_cut_point_4}'} , {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] } ],
              'score_cut_point_4'   : [ IsNumber, {IsMoreThan: '{score_cut_point_3}'} , {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE] } ],

        },
        BY_RULE: {
                    [ {NAME:'assert_SumWeight'}, {ASSERT: '{score_claim_1_weight} + {score_claim_2_weight}  + {score_claim_3_weight} +  {score_claim_4_weight} = 1.0' } ]
        }
     }
   }
 }
