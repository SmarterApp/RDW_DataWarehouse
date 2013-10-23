define [
  'jquery'
  'mustache'
  'jqGrid'
  'edwareUtil'
  'edwarePopulationBar'
  'edwareConfidenceLevelBar'
  'edwareLOSConfidenceLevelBar'
], ($, Mustache, jqGrid, edwareUtil, edwarePopulationBar, edwareConfidenceLevelBar, edwareLOSConfidenceLevelBar) ->

  EXPORT_TEMPLATE = "<div class='export'><span>{{value}}</span><span>{{title}}</span></div>"

  SUMMARY_TEMPLATE = "<div class='{{cssClass}}'><span class=summarySubtitle>{{subTitle}}:</span><br/><span class='summaryTitle'>{{summaryTitle}}</span>{{{export}}}</div>"

  POPULATION_BAR_TEMPLATE = "<div class='barContainer default'>" +
    "<div class='alignmentHighlightSection'><div class ='populationBar' data-margin-left='{{alignment}}'>{{{populationBar}}}</div></div>" +
    "<div class='studentsTotal'>{{total}}</div>" +
    "{{#unfilteredTotal}}<div class='unfilteredTotal'>{{ratio}}% of {{unfilteredTotal}}</div>{{/unfilteredTotal}}" +
    "<div class='alignmentLine' style='margin-left:{{alignmentLine}}px;'></div>" +
    "{{{export}}}" +
    "</div>"

  TEXT_TEMPLATE = "<div>{{value}}{{{export}}}</div>"

  NAME_TEMPLATE = "<div>" +
    "{{#isStateViewOrDistrictView}}" +
    "<div class='marginLeft20 paddingBottom17'>" +
    "{{#isSticky}}" +
    "<div class='removeIcon stickyCompareRemove' value='{{rowId}}' data-value='{{rowId}}'></div><label class='stickyRemoveLabel'>Remove</label>" +
    "{{/isSticky}}" +
    "{{^isSticky}}" +
    "<input class='stickyCheckbox' type='checkbox' value='{{rowId}}' data-value='{{rowId}}'></input><label class='stickyCompareLabel'>Compare</label>" +
    "{{/isSticky}}" +
    "</div>" +
    "{{/isStateViewOrDistrictView}}" +
    "{{{export}}}" +
    "<a class='{{cssClass}}' href='{{link}}?{{params}}'>{{displayValue}}</a>" +
    "</div>"

  TOOLTIP_TEMPLATE =  "<div class='losTooltip hide'><div class='js-popupTitle hide'>{{student_name}} | {{subject.asmt_type}} {{labels.overall_score}}</div><div class='summary'><div class='title left'>{{labels.overall_score}}</div><div class='score left' style='background:{{subject.score_bg_color}};color:{{subject.score_text_color}}'><span>{{subject.asmt_score}}</span></div><div class='description' style='color:{{subject.score_bg_color}}'>{{score_ALD}}</div></div><hr/><div class='losPerfBar'>{{{confidenceLevelBar}}}</div><div class='errorBand'>{{labels.error_band}}: <strong>{{subject.asmt_score_range_min}}-{{subject.asmt_score_range_max}}</strong></div></div>"

  PERFORMANCE_BAR_TEMPLATE = "<div class='asmtScore' style='background-color:{{subject.score_bg_color}}; color: {{subject.score_text_color}};'>{{subject.asmt_score}}{{{export}}}</div><div class = 'confidenceLevel'>{{{confidenceLevelBar}}}</div>{{{toolTip}}}"

  CONFIDENCE_TEMPLATE = "<div>{{{export}}}<strong>{{value}}</strong> (&#177;{{confidence}})</div>"

  #
  # * EDWARE grid formatters
  # * Handles all the methods for displaying cutpoints, link in the grid
  #
  buildUrl = (rowObject, options)->
    # Build url query param
    params = for k, v of rowObject.params
      k = options.colModel.formatoptions.id_name if k == "id"
      k + "=" + v
    params.join "&"

  # draw name columns
  showTooltip = (options, displayValue) ->
    (rowId, val, rawObject, cm, rdata) ->
      'title="' + displayValue + '"'

  showlink = (value, options, rowObject) ->

    # draw summary row (grid footer)
    isHeader = rowObject.header
    return Mustache.to_html SUMMARY_TEMPLATE, {
      cssClass: options.colModel.formatoptions.style
      subTitle: rowObject.subtitle
      summaryTitle: value
      export: formatExport(value, '')
    } if isHeader
    
    getDisplayValue = () ->
      displayValue = value
      if options.colModel.formatoptions.id_name is "asmtGrade"
        displayValue = "Grade " + value
      displayValue = $.jgrid.htmlEncode(displayValue)
      # Set cell value tooltip
      options.colModel.cellattr = showTooltip options, displayValue
      displayValue

    displayValue = getDisplayValue()
    # check if export current field
    exportValue = formatExport displayValue, "" if options.colModel.export

    # sticky comparison is not activated, show checkbox
    Mustache.to_html NAME_TEMPLATE, {
      isStateViewOrDistrictView: options.colModel.formatoptions.id_name in ["districtGuid", "schoolGuid"]
      isSticky: options.colModel.stickyCompareEnabled
      rowId: rowObject.id
      cssClass: options.colModel.formatoptions.style
      link: options.colModel.formatoptions.linkUrl
      params: buildUrl rowObject, options
      export: exportValue
      displayValue: displayValue
    }
  
  showStudentLink = (value, options, rowObject) ->
    # this formatter is used in los
    link = options.colModel.formatoptions.linkUrl
    displayValue = $.jgrid.htmlEncode(value)
    params = buildUrl rowObject, options
    showTooltip options, displayValue
    
    if not options.colModel.stickyCompareEnabled
      "<div class='marginLeft20'>" + 
      "<input class='stickyCheckbox marginRight10' id='sticky_" + rowObject.rowId + "' type='checkbox' data-value=\"" + rowObject.rowId + "\" data-name=\"" + displayValue + "\"></input>" + 
      "<a class='verticalAlignMiddle' href=\"" + link + "?" + params + "\">" + displayValue + "</a></div>"
    else
      "<div class='marginLeft20'><div class='removeIcon stickyCompareRemove marginRight10' data-value=\"" + rowObject.rowId + "\"></div>" + 
      "<a href=\"" + link + "?" + params + "\">" + displayValue + "</a>"

  showText = (value, options, rowObject) ->
    exportable = options.colModel.export

    return Mustache.to_html TEXT_TEMPLATE, {
      value: value,
      export: formatExport(value, '')
    } if exportable

    return value

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
    return '' if not subject

    confidence = subject[names[2]][names[3]]['confidence']
    Mustache.to_html CONFIDENCE_TEMPLATE, {
      value: value,
      confidence: confidence
      export: formatExport(value, '') if options.colModel.export
    }


  performanceBar = (value, options, rowObject) ->
    subject_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.assessments[subject_type]
    labels = options.colModel.labels
    return showText(value, options, rowObject) if not subject

    score_ALD = if not subject.cut_point_intervals[subject.asmt_perf_lvl-1] then "" else subject.cut_point_intervals[subject.asmt_perf_lvl-1]["name"]

    student_name = rowObject.student_first_name if rowObject.student_first_name
    student_name = student_name + " " + rowObject.student_middle_name[0] + "." if rowObject.student_middle_name
    student_name = student_name + " " + rowObject.student_last_name if rowObject.student_last_name

    toolTip = Mustache.to_html TOOLTIP_TEMPLATE, {
      student_name: student_name
      subject: subject
      labels: labels
      score_ALD: score_ALD
      confidenceLevelBar: edwareConfidenceLevelBar.create(subject, 300)
    }
    perfBar = Mustache.to_html PERFORMANCE_BAR_TEMPLATE, {
      subject: subject
      confidenceLevelBar: edwareLOSConfidenceLevelBar.create subject, 120
      toolTip: toolTip
      export: formatExport(value, '') if options.colModel.export
    }
    perfBar


  populationBar = (value, options, rowObject) ->
    asmt_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.results[asmt_type]

    # display empty message
    return '' if not subject
    # display insufficient data message
    text = options.colModel.labels['insufficient_data']
    return Mustache.to_html TEXT_TEMPLATE, {
      value: text,
      export: formatExport(text, subject.asmt_subject)
    } if parseInt(value) <= 0

    subject = formatSubject subject
    export_filed = options.colModel.export #check if export current field
    exportValue = formatExport subject.total, subject.asmt_subject if export_filed
    return Mustache.to_html POPULATION_BAR_TEMPLATE, {
      alignment: subject.alignment,
      alignmentLine: subject.alignmentLine,
      total: subject.total,
      unfilteredTotal: subject.unfilteredTotal,
      ratio: subject.ratio,
      populationBar: edwarePopulationBar.create(subject)
      export: exportValue
    }


  formatExport = (value, title) ->
    # escape double quote
    value = value.replace(/"/g, '\\"') if typeof(value) is 'string'
    #export fields
    Mustache.to_html EXPORT_TEMPLATE, {
      value: '"' + value + '"' if value
      title: title
    }


  formatSubject = (subject) ->
    subject.total = edwareUtil.formatNumber(subject.total)
    subject.unfilteredTotal = edwareUtil.formatNumber(subject.unfilteredTotal)
    ratio = subject.total * 100.0 / subject.unfilteredTotal
    subject.ratio = edwareUtil.formatNumber(Math.round(ratio))
    for interval in subject.intervals
      interval.count = edwareUtil.formatNumber(interval.count) if interval
    subject


  showlink: showlink
  showStudentLink: showStudentLink
  showText: showText
  showOverallConfidence: showOverallConfidence
  showConfidence: showConfidence
  performanceBar: performanceBar
  populationBar: populationBar
