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
    
    content = {}
    getContent "../data/content.json", (tempContent) ->
      content = tempContent
      
    edwareDataProxy.getDatafromSource "/data/individual_student_report", params, (data) ->
        
      # use template from file to display the json data  
      
      i = 0
      while i < data.items.length
      
        items = data.items[i]
        
        # Apply text color and background color for overall score summary info section
        
        items.count = i
      
        items.score_color = items.cut_points[items.asmt_perf_lvl-1].bg_color
        items.score_text_color = items.cut_points[items.asmt_perf_lvl-1].text_color
        items.score_bg_color = items.cut_points[items.asmt_perf_lvl-1].bg_color
        items.score_name = items.cut_points[items.asmt_perf_lvl-1].name

        # set role-based content
        items.content = content
        
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

  #
  # get role-based content
  #
  getContent = (configURL, callback) ->
      content = {}
      
      return false  if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
      
      $.getJSON configURL, (data) ->
        content = data.content

        if callback
          callback content
        else
          content

  generateIndividualStudentReport: generateIndividualStudentReport
