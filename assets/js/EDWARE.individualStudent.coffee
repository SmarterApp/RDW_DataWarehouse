#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "text!templates/individualStudent_report/individual_student_template.html"
  "text!templates/individualStudent_report/confidenceLevelBar.html"
  "text!templates/individualStudent_report/claimsInfo.html"
], ($, Mustache, edwareDataProxy, indivStudentReportTemplate, confidenceLevelBarTemplate, claimsInfoTemplate) ->
   
  #
  #    * Generate individual student report
  #    
  generateIndividualStudentReport = (params) ->
      
    edwareDataProxy.getDatafromSource "/data/individual_student_report", params, (data) ->
      
      # ELA
      data.items[0].asmt_score_min = 0
      data.items[0].asmt_score_max = 2500
      
      data.items[0].asmt_cut_point_percent_1 =  ((data.items[0].asmt_cut_point_1 - data.items[0].asmt_score_min) / data.items[0].asmt_score_max) * 100
      data.items[0].asmt_cut_point_percent_2 =  ((data.items[0].asmt_cut_point_2 - data.items[0].asmt_cut_point_1) / data.items[0].asmt_score_max) * 100
      data.items[0].asmt_cut_point_percent_3 =  ((data.items[0].asmt_cut_point_3 - data.items[0].asmt_cut_point_2) / data.items[0].asmt_score_max) * 100
      data.items[0].asmt_cut_point_percent_4 =  ((data.items[0].asmt_score_max - data.items[0].asmt_cut_point_3) / data.items[0].asmt_score_max) * 100
      
      data.items[0].asmt_score_pos = ((data.items[0].asmt_score / data.items[0].asmt_score_max) * 100)
      data.items[0].asmt_score_percent =  100 - data.items[0].asmt_score_pos
      
      # MATH
      
      data.items[1].asmt_score_min = 0
      data.items[1].asmt_score_max = 2800
      
      data.items[1].asmt_cut_point_percent_1 =  ((data.items[1].asmt_cut_point_1 - data.items[1].asmt_score_min) / data.items[1].asmt_score_max) * 100
      data.items[1].asmt_cut_point_percent_2 =  ((data.items[1].asmt_cut_point_2 - data.items[1].asmt_cut_point_1) / data.items[1].asmt_score_max) * 100
      data.items[1].asmt_cut_point_percent_3 =  ((data.items[1].asmt_cut_point_3 - data.items[1].asmt_cut_point_2) / data.items[1].asmt_score_max) * 100
      data.items[1].asmt_cut_point_percent_4 =  ((data.items[1].asmt_score_max - data.items[1].asmt_cut_point_3) / data.items[1].asmt_score_max) * 100
      
      data.items[1].asmt_score_pos = ((data.items[1].asmt_score / data.items[1].asmt_score_max) * 100)
      data.items[1].asmt_score_percent =  100 - data.items[1].asmt_score_pos
        
      # use template from file to display the json data  
      
      partials = 
        confidenceLevelBar: confidenceLevelBarTemplate
        claimsInfo: claimsInfoTemplate
      
      output = Mustache.to_html indivStudentReportTemplate, data, partials
      
      $("#individualStudentContent").html output

  generateIndividualStudentReport: generateIndividualStudentReport