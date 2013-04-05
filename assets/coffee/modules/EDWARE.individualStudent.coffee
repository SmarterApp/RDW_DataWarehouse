#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareDataProxy"
  "edwareConfidenceLevelBar"
  "text!templates/individualStudent_report/individual_student_template.html"
  "text!templates/individualStudent_report/claimsInfo.html"
  "edwareBreadcrumbs"
  "edwareHeader"
  "edwareUtil"
  "edwareFeedback"
  "edwareFooter"
], ($, bootstrap, Mustache, edwareDataProxy, edwareConfidenceLevelBar, indivStudentReportTemplate, claimsInfoTemplate, edwareBreadcrumbs, edwareHeader, edwareUtil, edwareFeedback, edwareFooter) ->
      
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
      
    # Get temporary CMS data from data/content.json file
    getContent "../data/content.json", (tempContent) ->
      content = tempContent
      
    # Get individual student report data from the server
    options =
      async: true
      method: "POST"
      params: params
      
    edwareDataProxy.getDatafromSource "/data/individual_student_report", options, (data) ->
   
      defaultColors = {}
      options =
        async: false
        method: "GET"
    
      edwareDataProxy.getDatafromSource "../data/color.json", options, (defaultColors) ->
      
        i = 0
        while i < data.items.length
          items = data.items[i]
          
          # if cut points don't have background colors, then it will use default background colors
          j = 0
          while j < items.cut_point_intervals.length
            if !items.cut_point_intervals[j].bg_color
              $.extend(items.cut_point_intervals[j], defaultColors[j])
            j++
          
          # Generate unique id for each assessment section. This is important to generate confidence level bar for each assessment
          # ex. assessmentSection0, assessmentSection1
          items.count = i
  
          # set role-based content
          items.content = content.content
          
  
          # Select cutpoint color and background color properties for the overall score info section
          performance_level = items.cut_point_intervals[items.asmt_perf_lvl-1]
          
          # Apply text color and background color for overall score summary info section
          items.score_color = performance_level.bg_color
          items.score_text_color = performance_level.text_color
          items.score_bg_color = performance_level.bg_color
          items.score_name = performance_level.name
          
          # set level-based overall ald content
          items.overall_ald = content.overall_ald[items.asmt_subject][items.asmt_perf_lvl]
          
          # set psychometric_implications content
          output = Mustache.render(content.psychometric_implications[items.asmt_subject], items)
          items.psychometric_implications = output
          
          # set policy content
          grade = content.policy_content[items.grade]
          if items.grade is "11"
            items.policy_content = grade[items.asmt_subject]
          else if items.grade is "3"
            grade_asmt = grade[items.asmt_subject]
            items.policy_content = grade_asmt[items.asmt_perf_lvl]
          
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
            
            claim.claim_score_weight = claimScoreWeightArray[claim.assessmentUC][j]
            
            claim.desc = content.claims[items.asmt_subject][claim.indexer]
            j++
          
          i++
          
        contextData = data.context
        $('#header').header()
        $('#breadcrumb').breadcrumbs(contextData)
        
        partials = 
          claimsInfo: claimsInfoTemplate
        
        # use mustache template to display the json data       
        output = Mustache.to_html indivStudentReportTemplate, data, partials     
        $("#individualStudentContent").html output
        
        renderClaimScoreRelativeDifference data
        
        # Generate Confidence Level bar for each assessment      
        i = 0
        while i < data.items.length
          item = data.items[i]       
          barContainer = "#assessmentSection" + i + " .confidenceLevel"
          edwareConfidenceLevelBar.create item, 640, barContainer        
          i++
        
        # Generate footer links
        $('#footer').generateFooter('individual_student_report')
        
        # append user_info (e.g. first and last name)
        if data.user_info
          $('#header .topLinks .user').html edwareUtil.getUserName data.user_info
          role = edwareUtil.getRole data.user_info
          uid = edwareUtil.getUid data.user_info
          edwareFeedback.renderFeedback(role, uid, "individual_student_report")

  #
  # render Claim Score Relative Difference (arrows)
  #
  renderClaimScoreRelativeDifference = (data) ->
    i = 0
    while i < data.items.length
      items = data.items[i]
      # find grand parent element ID
      assessmentSectionId = '#assessmentSection' + i
      claims = items.claims
      j = 0
      while j < claims.length
        claim = claims[j]
        # find parent element ID
        claimId = '#claim' + claim.indexer
        # create inner div and attache to the div(targetId)
        div_bar = $('<div/>')
        # if relative difference is positive, then render uppder div
        if claim.claim_score_relative_difference > 0
          # find target element ID
          contentId = '#content' + claim.indexer + '_upper'
          img = '../images/Claim_arrowhead_up.png'
          # style for vertical bar
          bar_height = Math.abs(claim.claim_score_relative_difference)
          image_y_position = 100 - Math.abs(claim.claim_score_relative_difference)
          # style for vertical bar
          div_bar.addClass("claim_score_arrow_bar claim_score_up_arrow_bar")
        else
          # find target element ID
          contentId = '#content' + claim.indexer + '_lower'
          img = '../images/Claim_arrowhead_down.png'
          bar_height = Math.abs(claim.claim_score_relative_difference)
          image_y_position = Math.abs(claim.claim_score_relative_difference)
          # style for vertical bar
          div_bar.addClass("claim_score_arrow_bar claim_score_down_arrow_bar")
          
          
        # specifying actual target element name
        targetId = assessmentSectionId + " " + claimId + " " + contentId
        # find center of "div" bar
        targetId_width = $(targetId).width()
        #bar width is 11
        div_bar_width = 11
        div_bar_center = (targetId_width/2.0-div_bar_width/2.0)/targetId_width*100.0
        div_bar.css("left", div_bar_center + "%")

        # find actual bar height
        targetId_height = $(targetId).height()
        # image height is 5
        adjusted_bar_height = bar_height - 5/targetId_height*100
        div_bar.css("height", adjusted_bar_height + "%")        
        # set Triangle image in target div
        $(targetId).css("background-image", "url(" + img + ")")
        $(targetId).css("background-position", "50% " + image_y_position + "%")
        $(targetId).append div_bar
        j++
      i++
  #
  # get role-based content
  #
  getContent = (configURL, callback) ->
      content = {}
      
      return false  if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
      
      options =
        async: false
        method: "GET"
      
      edwareDataProxy.getDatafromSource configURL, options, (data) ->
          content = data

          if callback
            callback content
          else
            content

  generateIndividualStudentReport: generateIndividualStudentReport
