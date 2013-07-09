define [
  'jquery'
  'jqGrid'
  'edwareUtil'
  'edwarePopulationBar'
  'edwareConfidenceLevelBar'
  'edwareLOSConfidenceLevelBar'  
], ($, jqGrid, edwareUtil, edwarePopulationBar, edwareConfidenceLevelBar, edwareLOSConfidenceLevelBar) ->
  #
  # * EDWARE grid formatters
  # * Handles all the methods for displaying cutpoints, link in the grid
  # 
  
  math_count = 1
  ela_count = 1
    
  showlink = (value, options, rowObject) ->
    link = options.colModel.formatoptions.linkUrl
    cssClass = options.colModel.formatoptions.style
    unless rowObject.header
      params = ""
      i = 0 
      for k, v of rowObject.params
        if (i != 0)
          params = params + "&"
        if k == "id"
          k = options.colModel.formatoptions.id_name
        params = params + k + "=" + v
        i++
      if options.colModel.formatoptions.id_name is "asmtGrade"
         "<a class="+cssClass+" href=\"" + link + "?" + params + "\">" + $.jgrid.htmlEncode("Grade " + value) + "</a>"
      else
        "<a class="+cssClass+" href=\"" + link + "?" + params + "\">" + $.jgrid.htmlEncode(value) + "</a>"
    else
      "<div class="+cssClass+"><span class=summarySubtitle>" + rowObject.subtitle + ":</span><br/><span class='summaryTitle'>"+value+"</span></div>"
  
  showOverallConfidence = (value, options, rowObject) ->
    names = options.colModel.name.split "."
    subject = rowObject[names[0]][names[1]]
    
    if subject
      "<div>P" + subject.asmt_perf_lvl + " [" + subject.asmt_score_range_min + "] " + value + " [" + subject.asmt_score_range_max + "]</div>"
    else
      ""
  
  showConfidence = (value, options, rowObject) ->
    names = options.colModel.name.split "."
    subject = rowObject[names[0]][names[1]]
    if subject
      confidence = subject[names[2]][names[3]]['confidence']
      "<div><strong>" + value + "</strong> (&#177;" + confidence + ")</div>"
    else
      ""
    
  performanceBar = (value, options, rowObject) ->
    asmt_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.assessments[asmt_type]
    if subject
      score_ALD = subject.cut_point_intervals[subject.asmt_perf_lvl-1]["name"]
      subject.score_color = subject.score_bg_color
      results =  edwareLOSConfidenceLevelBar.create subject, 120
      results2 =  edwareConfidenceLevelBar.create subject, 300
      
      student_name = rowObject.student_first_name if rowObject.student_first_name
      student_name = student_name + " " + rowObject.student_middle_name[0] + "." if rowObject.student_middle_name
      student_name = student_name + " " + rowObject.student_last_name if rowObject.student_last_name
      perfBar = "<div class='asmtScore' style='background-color:"+ subject.score_bg_color + "; color: "+ subject.score_text_color + ";'>" + subject.asmt_score + "</div><div class = 'confidenceLevel'>" +results+ "</div>"
      toolTip = "<div class='losTooltip hide'><div class='js-popupTitle hide'>"+student_name+ " | " + subject.asmt_type + " Overall Score</div>"
      toolTip = toolTip + "<div class='summary'><div class='title left'>Overall Score</div><div class='score left' style='background:"+subject.score_bg_color+";color:"+subject.score_text_color+"'><span>"+subject.asmt_score+"</span></div><div class='description' style='color:"+subject.score_bg_color+"'>"+score_ALD+"</div></div><hr/><div class='losPerfBar'>"+results2+"</div><div class='errorBand'>Error Band: <strong>"+subject.asmt_score_range_min+"-"+subject.asmt_score_range_max+"</strong></div></div>"
        
      output = perfBar + toolTip   
    else
      ""   

  populationBar = (value, options, rowObject) ->
    asmt_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.results[asmt_type]
    align_button_class = $(".align_button").attr("class")
    
    output = ""
    if subject
      results = edwarePopulationBar.create subject
      if align_button_class.indexOf("align_on") isnt -1
        output = "<div class='barContainer'><div class='alignmentHighlightSection'><div class = 'populationBar' style='margin-left:" + subject.alignment + "px;'>" + results + "</div></div><div class='studentsTotal'>" + subject.total + "</div><div class='alignmentLine' style='margin-left:" + subject.alignmentLine + "px;'></div></div>"
          
      else
        output = "<div class='barContainer'><div class = 'populationBar'>" + results + "</div><div class='studentsTotal'>" + subject.total + "</div><div class='alignmentLine' style='margin-left:" + subject.alignmentLine + "px;'></div></div>"
      
      output

  showlink: showlink
  showOverallConfidence: showOverallConfidence
  showConfidence: showConfidence
  performanceBar: performanceBar
  populationBar: populationBar
