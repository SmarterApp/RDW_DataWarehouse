#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareConfidenceLevelBar"
  "text!templates/individualStudent_report/individual_student_template.html"
  "text!templates/individualStudent_report/claimsInfo.html"
  "cs!edwareBreadcrumbs"
  "cs!edwareUtil"
], ($, Mustache, edwareDataProxy, edwareConfidenceLevelBar, indivStudentReportTemplate, claimsInfoTemplate, edwareBreadcrumbs, edwareUtil) ->
  
  default_cutPointColors = [{
          "text_color": "#ffffff",
          "bg_color": "#DD514C",
          "start_gradient_bg_color": "#EE5F5B",
          "end_gradient_bg_color": "#C43C35"
      }, {
          "text_color": "#000",
          "bg_color": "#e4c904",
          "start_gradient_bg_color": "#e3c703",
          "end_gradient_bg_color": "#eed909"
      }, {
          "text_color": "#ffffff",
          "bg_color": "#3b9f0a",
          "start_gradient_bg_color": "#3d9913",
          "end_gradient_bg_color": "#65b92c"
      }, {
          "text_color": "#ffffff",
          "bg_color": "#237ccb",
          "start_gradient_bg_color": "#2078ca",
          "end_gradient_bg_color": "#3a98d1"
      }]
      
  # claim score weight in percentage
  claimScoreWeightArray = {
    "MATH": ["40", "40", "20", "10"],
    "ELA": ["40", "30", "20", "10"]
  }
  
  #
  #    * Generate individual student report
  #    
  generateIndividualStudentReport = (params) ->
    
    content = {}
      
    getContent "../data/content.json", (tempContent) ->
      content = tempContent
      
    edwareDataProxy.getDatafromSource "/data/individual_student_report", params, (data) ->
      
      i = 0
      while i < data.items.length
        items = data.items[i]
        
        # if cut points don't have background colors, then it will use default background colors
        j = 0
        while j < items.cut_point_intervals.length
          if !items.cut_point_intervals[j].bg_color
            $.extend(items.cut_point_intervals[j], default_cutPointColors[j])
          j++
        
        # Generate unique id for each assessment section. This is important to generate confidence level bar for each assessment
        # ex. assessmentSection0, assessmentSection1
        items.count = i

        # set role-based content
        items.content = content

        # Select cutpoint color and background color properties for the overall score info section
        performance_level = items.cut_point_intervals[items.asmt_perf_lvl-1]
        
        # Apply text color and background color for overall score summary info section
        items.score_color = performance_level.bg_color
        items.score_text_color = performance_level.text_color
        items.score_bg_color = performance_level.bg_color
        items.score_name = performance_level.name
        
        # Claim section
        # For less than 4 claims, width of the claim box would be 28%
        # For 4 claims, the width of the claim box would be 20%
        items.claim_box_width = "28%" if items.claims.length < 4
        items.claim_box_width = "20%" if items.claims.length == 4
        
        
        # Add claim score weight 
        j = 0
        while j < items.claims.length
          claim = items.claims[j]
          claim.assessmentUC = items.asmt_subject.toUpperCase()
          
          # Temporary fix for displaying claim number
          claim.number = "Claim " + claim.indexer
          claim.number = "Claim 2 & 4" if claim.indexer is "2" and claim.assessmentUC is "MATH"
          
          
          claim.claim_score_weight = claimScoreWeightArray[claim.assessmentUC][j]
          j++
        
        i++
        
      contextData = data.context
      
      breadcrumbsData = {}
        
      edwareUtil.readJson "../data/student_breadcrumbs.json", (tempData) ->
        breadcrumbsData = tempData
        
      # for each breadcrumb item
      # item.name = contextData[item.field_name]
      # if item.field_name = 'grade', update item.link
      
      arr = breadcrumbsData['items']
      length = arr.length
      element = null
      i = 0
      
      while i < length
        element = arr[i]
        element.name = contextData[element.field_name]
        if element.field_name == 'grade'
          element.link = element.link + "?districtId=" + contextData['district_id'] + "&schoolId=" + contextData['school_id']+ "&asmtGrade=" + contextData['grade']
        if element.field_name == 'student_name'
          # add 's to student name. if name ends in s, only add '.
          if element.name.substr(element.name.length - 1) == 's'
            element.name = element.name + "'"
          else
            element.name = element.name + "'s"
          element.name = element.name + " Results"
        i++

      $('#breadcrumb').breadcrumbs(breadcrumbsData)

      partials = 
        claimsInfo: claimsInfoTemplate
      
      # use mustache template to display the json data       
      output = Mustache.to_html indivStudentReportTemplate, data, partials     
      $("#individualStudentContent").html output
      
      # Generate Confidence Level bar for each assessment      
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
      
      $.ajax
        url: configURL
        dataType: "json"
        async: false
        success: (data) ->
          content = data.content

          if callback
            callback content
          else
            content
            
  #
  #    * Get breadcrumbs data
  # 
  # readBreadcrumbs = (templateURL, callback) ->
      # return false if templateURL is "undefined" or typeof templateURL is "number" or typeof templateURL is "function" or typeof templateURL is "object"
#         
      # $.ajax
        # url: templateURL
        # dataType: "json"
        # async: false
        # success: (data) ->
          # content = data
# 
          # if callback
            # callback content
          # else
            # content

  generateIndividualStudentReport: generateIndividualStudentReport
