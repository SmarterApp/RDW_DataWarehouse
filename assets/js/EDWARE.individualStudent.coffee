#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareUtil"
  "text!templates/individual_student_template.html"
], ($, Mustache, edwareDataProxy, edwareUtil, indivStudentReportTemplate) ->
   
  #
  #    * Generate individual student report
  #    
  generateIndividualStudentReport = (params) ->
      
    getIndividualStudentReport "/data/individual_student_report", params, (studentData) -> 
        output = Mustache.to_html indivStudentReportTemplate, studentData
        $("#assesmentInfo").html output

  getIndividualStudentReport = (sourceURL, params, callback) ->
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    edwareDataProxy.getDatafromSource sourceURL, params, (data) ->
      
      studentData = data
      if callback
        callback studentData
      else
        studentData

  generateIndividualStudentReport: generateIndividualStudentReport