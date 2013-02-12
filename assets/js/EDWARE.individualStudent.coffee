#global define
define [
  "jquery"
  "cs!edwareDataProxy"
  "cs!edwareUtil"
], ($, edwareDataProxy, edwareUtil) ->
   
  #
  #    * Create Student data grid
  #    
      
  generateIndividualStudentReport = (params) ->
      
    getIndividualStudentReport "/data/individual_student_report", params, (studentData) -> 
    
        $("#assessmentTitle").html studentData.asmt_subject
        $("#assessmentPeriod").html studentData.asmt_period
        $("#techerName").html studentData.teacher_last_name
        $("#assessmentDate").html studentData.date_taken_day
 

  getIndividualStudentReport = (sourceURL, params, callback) ->
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    edwareDataProxy.getDatafromSource sourceURL, params, (data) ->
      
      studentData = data[0]
      if callback
        callback studentData
      else
        studentData

  generateIndividualStudentReport: generateIndividualStudentReport