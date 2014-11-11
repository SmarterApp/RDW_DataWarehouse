define [], () ->

  REPORT_NAME: {
    CPOP: 'comparing_populations'
    LOS:  'list_of_students'
    ISR:  'individual_student_report'
  }

  REPORT_TYPE: {
    STATE: 'state'
    DISTRICT: 'district'
    SCHOOL: 'school'
    GRADE: 'grade'
  }

  REPORT_JSON_NAME: {
    CPOP: 'comparingPopulationsReport'
    LOS: 'studentList'
    ISR: 'indivStudentReport'
  }

  DELIMITOR: {
    COMMA: ','
    NEWLINE: '\n'
  }

  ASMT_TYPE: {
    SUMMATIVE: 'Summative'
    INTERIM: 'Interim Comprehensive'
    IAB: 'Interim Assessment Blocks'
    'INTERIM COMPREHENSIVE': 'Interim Comprehensive'
    'INTERIM ASSESSMENT BLOCKS': 'Interim Assessment Blocks'
    'Summative': 'Summative'
    'Interim Comprehensive': 'Interim'
    'Interim Assessment Blocks': 'IAB'
  }

  ASMT_VIEW: {
    OVERVIEW: "Math_ELA",
    MATH: "Math",
    ELA: "ELA"
  }

  EVENTS: {
    SORT_COLUMNS: 'edwareOnSortColumns'
    EXPAND_COLUMN: 'edwareOnExpandColumn'
  }

  KEYS: {
    F: 70
    ENTER: 13
    ESC: 27
    UP_ARROW: 38
    DOWN_ARROW: 40
  }

  SUBJECT_TEXT: {
    Math: "Mathematics"
    ELA: "ELA/Literacy"
  }

  INDEX_COLUMN: {
    LOS: "student_full_name"
  }

  SUBJECTS: ['Math', 'ELA']

  ASMT_TYPES: ["SUMMATIVE", "INTERIM COMPREHENSIVE"]
