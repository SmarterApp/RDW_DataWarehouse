#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareConfidenceLevelBar"
  "text!templates/individualStudent_report/individual_student_template.html"
  "text!templates/individualStudent_report/claimsInfo.html"
], ($, Mustache, edwareDataProxy, edwareConfidenceLevelBar, indivStudentReportTemplate, claimsInfoTemplate) ->
    
  #
  #    * Generate individual student report
  #    
  generateIndividualStudentReport = (params) ->
      
    edwareDataProxy.getDatafromSource "/data/individual_student_report", params, (data) ->
        
      # use template from file to display the json data  
      
      i = 0
      while i < data.items.length
      
        items = data.items[i]
        
        # apply text color and background color for overall score
        
        items.count = i
      
        items.score_color = items.cut_points[items.asmt_perf_lvl-1].bg_color
        items.score_text_color = items.cut_points[items.asmt_perf_lvl-1].text_color
        items.score_bg_color = items.cut_points[items.asmt_perf_lvl-1].bg_color
        items.score_name = items.cut_points[items.asmt_perf_lvl-1].name
        
        i++
        
      partials = 
        claimsInfo: claimsInfoTemplate
      
      output = Mustache.to_html indivStudentReportTemplate, data, partials
      
      $("#individualStudentContent").html output
      
      i = 0
      
      while i < data.items.length
        
        item = data.items[i]
        
        barContainer = "#assessmentSection" + i + " .confidenceLevel"
        edwareConfidenceLevelBar.create barContainer, item
        
        i++

  generateIndividualStudentReport: generateIndividualStudentReport