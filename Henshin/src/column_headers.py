# Abbreviations:
SI = 'Student Identifier'
AI = 'Assessment Identifiers'
OA = 'Overall'
CL = 'Claim'

# Column Headers and types:
# list index keeps the order of columns
# each tuple in list: (landing_zone_column_name, schema_column_name)
COLUMN_MAP_INFO = [('SI-state-code', 'state_code'),
                      ('SI-district-id', 'district_guid'),
                      ('SI-school-id', 'school_guid'),
                      ('SI-teacher-id', 'teacher_guid'),
                      ('SI-student-grade', 'enrl_grade'),
                      ('SI-section-id', 'section_guid'),
                      ('SI-student-id', 'student_guid'),
                      ('AI-asmt-id', 'asmt_rec_id'),
                      ('AI-date-taken', 'date_taken'),
                      ('AI-where-taken', 'where_taken_guid'),
                      ('OA-score', 'asmt_score'),
                      ('OA-CI-left', 'asmt_score_range_min'),
                      ('OA-CI-right', 'asmt_score_range_max'),
                      ('CL-1-claim', 'asmt_claim_1_score'),
                      ('CL-1-CI-left', 'asmt_claim_1_score_range_min'),
                      ('CL-1-CI-right', 'asmt_claim_1_score_range_max'),
                      ('CL-2-claim', 'asmt_claim_2_score'),
                      ('CL-2-CI-left', 'asmt_claim_2_score_range_min'),
                      ('CL-2-CI-right', 'asmt_claim_2_score_range_max'),
                      ('CL-3-claim', 'asmt_claim_3_score'),
                      ('CL-3-CI-left', 'asmt_claim_3_score_range_min'),
                      ('CL-3-CI-right', 'asmt_claim_3_score_range_max'),
                      ('CL-4-claim', 'asmt_claim_4_score'),
                      ('CL-4-CI-left', 'asmt_claim_4_score_range_min'),
                      ('CL-4-CI-right', 'asmt_claim_4_score_range_max'),
                      ]
