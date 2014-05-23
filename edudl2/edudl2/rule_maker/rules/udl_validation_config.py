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
        BY_COLUMN: {'guid_batch': [],
                    'src_file_rec_num': [],
                    'guid_asmt': [[IsNotNull], IsGoodGUID],
                    'guid_asmt_location': [IsGoodGUID, {IsUniqueWithin: ['name_asmt_location']}],
                    'name_asmt_location': IsNotNull,
                    'grade_asmt': [IsNotNull, {IsInList: [3, 4, 5, 6, 7, 8, 11]}],
                    'name_state': [IsNotNull, {HasMaxLength: 32}],
                    'code_state': [IsNotNull, {IsInList: ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
                                                          'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
                                                          'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
                                                          'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']}],
                    'guid_district': [IsNotNull, IsGoodGUID],
                    'name_district': [IsNotNull, {HasMaxLength: DEFAULT_MAX_LENGTH}, {IsUniqueWithin: 'guid_district'}],
                    'guid_school': [IsNotNull, IsGoodGUID],
                    'name_school': [IsNotNull, {HasMaxLength: DEFAULT_MAX_LENGTH}],
                    'guid_student': [IsNotNull, IsGoodGUID,
                                     {IsUniqueWithin: ['name_student_first', 'name_student_middle',
                                                       'name_student_last', 'sex_student', 'email_student']}],
                    'name_student_first': [IsNotNull, IsSQLSafe, {HasMaxLength: DEFAULT_MAX_LENGTH}],
                    'name_student_middle': [IsSQLSafe, {HasMaxLength: DEFAULT_MAX_LENGTH}],
                    'name_student_last': [IsNotNull, IsSQLSafe, {HasMaxLength: DEFAULT_MAX_LENGTH}],
                    'sex_student': [IsNotNull, {IsInList: ['male', 'female']}],
                    'email_student': [IsNotNull, IsGoodEmail, {HasMaxLength: DEFAULT_MAX_LENGTH}],
                    'birthdate': [IsNotNull, IsGoodDate],
                    'grade_enrolled': {IsInList: [3, 4, 5, 6, 7, 8, 11]},
                    'date_assessed': [IsNotNull, IsGoodDate],
                    'score_asmt': [IsNotNull, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_asmt_min': [IsNotNull, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_asmt_max': IsNotNull,
                    'score_perf_level': [IsNotNull, {IsInList: [1, 2, 3, 4]}],
                    'score_claim_1': [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_claim_1_min': [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_claim_1_max': IsNumber,
                    'score_claim_2': [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_claim_2_min': [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_claim_2_max': IsNumber,
                    'score_claim_3': [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_claim_3_min': [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_claim_3_max': IsNumber,
                    'score_claim_4': [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_claim_4_min': [IsNumber, {IsInRange: [MIN_ASMT_SCORE, MAX_ASMT_SCORE]}],
                    'score_claim_4_max': IsNumber,
                    'guid_staff': [IsNotNull, IsGoodGUID],
                    'name_staff_first': [IsNotNull, {HasMaxLength: DEFAULT_MAX_LENGTH}],
                    'name_staff_middle': {HasMaxLength: DEFAULT_MAX_LENGTH},
                    'name_staff_last': [IsNotNull, {HasMaxLength: DEFAULT_MAX_LENGTH}],
                    'type_staff': [IsNotNull, {IsInList: ['Teacher', 'Staff']},
                                   {IsUniqueWithin: ['guid_staff', 'name_staff_first', 'name_staff_middle', 'name_staff_last']}],
                    },
        BY_RULE: {

        }
    }
}
