#global define
define ["jquery", "cs!widgets/EDWARE.grid.tablegrid"], ($, edwareGrid) ->
  
  columnData = []
  columnItems = []
  
  createStudentGrid = ->
    columnItems = [
      name: "Student"
      index: "Student"
      field: "student_fullname"
      width: 150
      style: "ui-ellipsis"
      hidden: true
    ,
      name: "Grade"
      index: "Grade"
      field: "enrollment_grade"
      width: 50
      sorttype: "int"
      align: "center"
      resizable: false
    ,
      name: "Math"
      items: [
        name: "Teacher"
        index: "Teacher"
        field: "assessments.MATH.teacher_fullname"
        width: 150
        style: "ui-ellipsis"
        resizable: false
      ,
        name: "Grade"
        index: "Grade"
        field: "assessments.MATH.asmt_grade"
        width: 50
        sorttype: "int"
        align: "center"
        resizable: false
      ,
        name: "Overall"
        index: "Overall"
        field: "assessments.MATH.asmt_score"
        width: 50
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 1"
        index: "Claim 1"
        field: "assessments.MATH.asmt_claim_1_score"
        width: 55
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 2"
        index: "Claim 2"
        field: "assessments.MATH.asmt_claim_2_score"
        width: 55
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 3"
        index: "Claim 3"
        field: "assessments.MATH.asmt_claim_3_score"
        width: 55
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 4"
        index: "Claim 4"
        field: "assessments.MATH.asmt_claim_4_score"
        width: 55
        formatter: "number"
        sorttype: "int"
        align: "right"
      ]
    ,
      name: "ELA"
      items: [
        name: "Teacher"
        index: "Teacher"
        field: "assessments.ELA.teacher_fullname"
        width: 150
        style: "ui-ellipsis"
        resizable: false
      ,
        name: "Grade"
        index: "Grade"
        field: "assessments.ELA.asmt_grade"
        width: 50
        sorttype: "int"
        align: "center"
        resizable: false
      ,
        name: "Overall"
        index: "Overall"
        field: "assessments.ELA.asmt_score"
        width: 50
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 1"
        index: "Claim 1"
        field: "assessments.ELA.asmt_claim_1_score"
        width: 55
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 2"
        index: "Claim 2"
        field: "assessments.ELA.asmt_claim_2_score"
        width: 55
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 3"
        index: "Claim 3"
        field: "assessments.ELA.asmt_claim_3_score"
        width: 55
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 4"
        index: "Claim 4"
        field: "assessments.ELA.asmt_claim_4_score"
        width: 55
        formatter: "number"
        sorttype: "int"
        align: "right"
      ]
    ]
    edwareGrid.create "gridTable", columnItems, columnData
    
  getStudentData = (soureURL) ->
    return false  if soureURL is `undefined` or soureURL is "" or typeof soureURL is "number"
    
    $.get soureURL, (data) ->
      columnData = data
      createStudentGrid()

  initialize = ->
    $(document).ready ->
      getStudentData "../data/student.json"

  initialize: initialize
