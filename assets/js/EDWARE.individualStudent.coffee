#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "text!templates/individual_student_template.html"
], ($, Mustache, edwareDataProxy, indivStudentReportTemplate) ->
   
  #
  #    * Generate individual student report
  #    
  generateIndividualStudentReport = (params) ->
      
    edwareDataProxy.getDatafromSource "/data/individual_student_report", params, (data) ->    
      output = Mustache.to_html indivStudentReportTemplate, data
      $("#assesmentInfo").html output

  generateIndividualStudentReport: generateIndividualStudentReport