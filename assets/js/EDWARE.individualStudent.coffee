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
      
      #$.extend data.items[0], cutpoints.ELA
      #$.extend data.items[1], cutpoints.MATH
        
      # use template from file to display the json data    
      output = Mustache.to_html indivStudentReportTemplate, data
      
      $("#individualStudentContent").html output

  generateIndividualStudentReport: generateIndividualStudentReport