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
  generateConfidenceLvlCutPointsPercent = (data) ->
    
    # ELA
    
      i = 0
      while i < data.items.length
        
        items = data.items[i]
        
        items.cut_points[0].asmt_cut_point_percent =  ((items.cut_points[0].cut_point - items.asmt_score_min) / items.asmt_score_max) * 100
        items.cut_points[1].asmt_cut_point_percent =  ((items.cut_points[1].cut_point - items.cut_points[0].cut_point) / items.asmt_score_max) * 100
        items.cut_points[2].asmt_cut_point_percent =  ((items.cut_points[2].cut_point - items.cut_points[1].cut_point) / items.asmt_score_max) * 100
        items.cut_points[3].asmt_cut_point_percent =  ((items.asmt_score_max - items.cut_points[2].cut_point) / items.asmt_score_max) * 100
        
        items.asmt_score_pos = ((items.asmt_score / items.asmt_score_max) * 100)
        items.asmt_score_percent =  100 - items.asmt_score_pos
        
        i++
    
  #
  #    * Generate individual student report
  #    
  generateIndividualStudentReport = (params) ->
      
    edwareDataProxy.getDatafromSource "/data/individual_student_report", params, (data) ->
      
      generateConfidenceLvlCutPointsPercent data
        
      # use template from file to display the json data  
      
      partials = 
        confidenceLevelBar: confidenceLevelBarTemplate
        claimsInfo: claimsInfoTemplate
      
      output = Mustache.to_html indivStudentReportTemplate, data, partials
      
      $("#individualStudentContent").html output

  generateIndividualStudentReport: generateIndividualStudentReport