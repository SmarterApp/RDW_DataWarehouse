#global define
define ["jquery", "cs!widgets/EDWARE.grid.tablegrid"], ($, edwareGrid) ->
  
  columnData = []
  columnItems = []
  assessmentCutpoints = {}
  
  getStudentData = (soureURL, callback) ->
    return false  if soureURL is `undefined` or soureURL is "" or typeof soureURL is "number"
      
    myData =
      districtId: 2
      schoolId: 1
      asmtGrade: "1" 
    
    $.ajax(
      type: "POST"
      url: "/data/list_of_students"
      data:
        JSON.stringify(myData);
      dataType: "json"
      contentType: "application/json"
    ).done (data) ->
      columnData = data
      callback()
      
  createStudentGrid = ->
    columnItems = [
      name: "Student"
      index: "Student"
      field: "student_full_name"
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
        field: "assessments.MATH.teacher_full_name"
        width: 100
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
        align: "center"
        style:"color-widget-red"
      ,
        name: "Claim 1"
        index: "Claim 1"
        field: "assessments.MATH.asmt_claim_1_score"
        width: 60
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 2"
        index: "Claim 2"
        field: "assessments.MATH.asmt_claim_2_score"
        width: 60
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 3"
        index: "Claim 3"
        field: "assessments.MATH.asmt_claim_3_score"
        width: 60
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 4"
        index: "Claim 4"
        field: "assessments.MATH.asmt_claim_4_score"
        width: 60
        formatter: "number"
        sorttype: "int"
        align: "right"
      ]
    ,
      name: "ELA"
      items: [
        name: "Teacher"
        index: "Teacher"
        field: "assessments.ELA.teacher_full_name"
        width: 100
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
        align: "center"
        style:"color-widget-yellow"
      ,
        name: "Claim 1"
        index: "Claim 1"
        field: "assessments.ELA.asmt_claim_1_score"
        width: 60
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 2"
        index: "Claim 2"
        field: "assessments.ELA.asmt_claim_2_score"
        width: 60
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 3"
        index: "Claim 3"
        field: "assessments.ELA.asmt_claim_3_score"
        width: 60
        formatter: "number"
        sorttype: "int"
        align: "right"
      ,
        name: "Claim 4"
        index: "Claim 4"
        field: "assessments.ELA.asmt_claim_4_score"
        width: 60
        formatter: "number"
        sorttype: "int"
        align: "right"
      ]
    ]
    
    getStudentData "../data/student.json", ->
      edwareGrid.create "gridTable", columnItems, columnData, assessmentCutpoints
    

  initialize = ->
    $(document).ready ->
      createStudentGrid()

  initialize: initialize
