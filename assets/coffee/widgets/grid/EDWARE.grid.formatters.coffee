define [
  'jquery'
  'mustache'
  'jqGrid'
  'edwareUtil'
  'edwarePopulationBar'
  'edwareConfidenceLevelBar'
  'edwareLOSConfidenceLevelBar'
  'edwareLanguage'
], ($, Mustache, jqGrid, edwareUtil, edwarePopulationBar, edwareConfidenceLevelBar, edwareLOSConfidenceLevelBar, i18n) ->

  POPULATION_BAR_TEMPLATE = "<div class='barContainer default'><div class='alignmentHighlightSection'><div class ='populationBar' data-margin-left='{{alignment}}'>{{{populationBar}}}</div></div><div class='studentsTotal'>{{total}}</div>{{#unfilteredTotal}}<div class='unfilteredTotal'>{{ratio}}% of {{unfilteredTotal}}</div>{{/unfilteredTotal}}<div class='alignmentLine' style='margin-left:{{alignmentLine}}px;'></div></div>"

  
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
    labels = options.colModel.labels
    if subject
      score_ALD = if not subject.cut_point_intervals[subject.asmt_perf_lvl-1] then "" else subject.cut_point_intervals[subject.asmt_perf_lvl-1]["name"] 
      subject.score_color = subject.score_bg_color
      results =  edwareLOSConfidenceLevelBar.create subject, 120
      results2 =  edwareConfidenceLevelBar.create subject, 300
      
      student_name = rowObject.student_first_name if rowObject.student_first_name
      student_name = student_name + " " + rowObject.student_middle_name[0] + "." if rowObject.student_middle_name
      student_name = student_name + " " + rowObject.student_last_name if rowObject.student_last_name
      perfBar = "<div class='asmtScore' style='background-color:"+ subject.score_bg_color + "; color: "+ subject.score_text_color + ";'>" + subject.asmt_score + "</div><div class = 'confidenceLevel'>" +results+ "</div>"
      toolTip = "<div class='losTooltip hide'><div class='js-popupTitle hide'>"+student_name+ " | " + subject.asmt_type + " " + labels.overall_score + "</div>"
      toolTip = toolTip + "<div class='summary'><div class='title left'>" + labels.overall_score + "</div><div class='score left' style='background:"+subject.score_bg_color+";color:"+subject.score_text_color+"'><span>"+subject.asmt_score+"</span></div><div class='description' style='color:"+subject.score_bg_color+"'>"+score_ALD+"</div></div><hr/><div class='losPerfBar'>"+results2+"</div><div class='errorBand'>" + labels.error_band + ": <strong>"+subject.asmt_score_range_min+"-"+subject.asmt_score_range_max+"</strong></div></div>"
        
      output = perfBar + toolTip
    else
      "" 

  populationBar = (value, options, rowObject) ->
    if parseInt(value) <= 0
      return i18n.getMessage('insufficient.data')

    asmt_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.results[asmt_type]
    if not subject
      return ""

    subject = formatSubject subject
    return Mustache.to_html POPULATION_BAR_TEMPLATE, {
      alignment: subject.alignment,
      alignmentLine: subject.alignmentLine,
      total: subject.total,
      unfilteredTotal: subject.unfilteredTotal,
      ratio: subject.ratio,
      populationBar: edwarePopulationBar.create(subject)
    }

  formatSubject = (subject)->
    subject.total = edwareUtil.formatNumber(subject.total)
    subject.unfilteredTotal = edwareUtil.formatNumber(subject.unfilteredTotal)
    ratio = subject.total * 100.0 / subject.unfilteredTotal
    subject.ratio = edwareUtil.formatNumber(Math.round(ratio))
    for interval in subject.intervals
      interval.count = edwareUtil.formatNumber(interval.count) if interval
    subject

  showlink: showlink
  showOverallConfidence: showOverallConfidence
  showConfidence: showConfidence
  performanceBar: performanceBar
  populationBar: populationBar
