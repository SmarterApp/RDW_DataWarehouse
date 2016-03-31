###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

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
    TAB: 9
  }

  SUBJECT_TEXT: {
    Math: "Mathematics"
    ELA: "ELA/Literacy"
    subject1: "Mathematics"
    subject2: "ELA/Literacy"
  }

  INDEX_COLUMN: {
    LOS: "student_full_name"
  }

  SUBJECTS: ['Math', 'ELA']

  ASMT_TYPES: ["SUMMATIVE", "INTERIM COMPREHENSIVE"]
