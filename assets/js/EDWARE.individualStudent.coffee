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
  #    * Generate confidence level bar cutpoint percentage width, score position, score percentage and
  #    * score text color, score background color, confidence level for overall score summary section
  #    
  generateConfidenceLvlCutPoints = (data) ->
    
      i = 0
      while i < data.items.length
        
        items = data.items[i]
        
        j = 0
        while j < items.cut_points.length
          
          if j == 0
            items.cut_points[j].asmt_cut_point_percent =  ((items.cut_points[j].cut_point - items.asmt_score_min) / items.asmt_score_max) * 100
          
          else if j == items.cut_points.length - 1
            items.cut_points[j].asmt_cut_point_percent =  ((items.asmt_score_max - items.cut_points[j-1].cut_point) / items.asmt_score_max) * 100
          
          else
            items.cut_points[j].asmt_cut_point_percent =  ((items.cut_points[j].cut_point - items.cut_points[j-1].cut_point) / items.asmt_score_max) * 100
        
          j++
        
        items.asmt_score_pos = ((items.asmt_score - (items.asmt_score_interval / 2)) / items.asmt_score_max) * 100
        items.asmt_min_score_percent = 100 - (((items.asmt_score - items.asmt_score_interval) / items.asmt_score_max) * 100)
        items.asmt_max_score_percent = ((items.asmt_score + items.asmt_score_interval) / items.asmt_score_max) * 100
        
        
        # apply text color and background color for overall score
        
        items.score_color = items.cut_points[items.asmt_perf_lvl-1].bg_color
        items.score_text_color = items.cut_points[items.asmt_perf_lvl-1].text_color
        items.score_bg_color = items.cut_points[items.asmt_perf_lvl-1].bg_color
        items.score_name = items.cut_points[items.asmt_perf_lvl-1].name
        
        i++
    
  #
  #    * Generate individual student report
  #    
  generateIndividualStudentReport = (params) ->
      
    edwareDataProxy.getDatafromSource "/data/individual_student_report", params, (data) ->
      
      generateConfidenceLvlCutPoints data
        
      # use template from file to display the json data  
      
      partials = 
        confidenceLevelBar: confidenceLevelBarTemplate
        claimsInfo: claimsInfoTemplate
      
      output = Mustache.to_html indivStudentReportTemplate, data, partials
      
      $("#individualStudentContent").html output

  generateIndividualStudentReport: generateIndividualStudentReport