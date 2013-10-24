define [
  'jquery'
  'mustache'
  'jqGrid'
  'edwareUtil'
  'edwarePopulationBar'
  'edwareConfidenceLevelBar'
  'edwareLOSConfidenceLevelBar'
  'text!edwareFormatterTemplate'
], ($, Mustache, jqGrid, edwareUtil, edwarePopulationBar, edwareConfidenceLevelBar, edwareLOSConfidenceLevelBar, edwareFormatterTemplate) ->

  getTemplate = (name) ->
    $(edwareFormatterTemplate).find('div#' + name).html()

  EXPORT_TEMPLATE = getTemplate('EXPORT_TEMPLATE')

  SUMMARY_TEMPLATE = getTemplate('SUMMARY_TEMPLATE')

  POPULATION_BAR_TEMPLATE = getTemplate('POPULATION_BAR_TEMPLATE')

  NAME_TEMPLATE = getTemplate('NAME_TEMPLATE')

  TOOLTIP_TEMPLATE = getTemplate('TOOLTIP_TEMPLATE')

  CONFIDENCE_TEMPLATE = getTemplate('CONFIDENCE_TEMPLATE')

  TEXT_TEMPLATE = getTemplate('TEXT_TEMPLATE')

  PERFORMANCE_BAR_TEMPLATE = getTemplate('PERFORMANCE_BAR_TEMPLATE')

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
    exportable = options.colModel.export #check if export current field
    
    # draw summary row (grid footer)
    isHeader = rowObject.header
    return Mustache.to_html SUMMARY_TEMPLATE, {
      cssClass: options.colModel.formatoptions.style
      subTitle: rowObject.subtitle
      summaryTitle: value
      columnName: options.colModel.columnName
      export: 'export' if exportable
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
    params = buildUrl(rowObject, options)
    # for some reason, link doesn't work well in old version of FF, have to construct manually here
    link = "<a href='" + options.colModel.formatoptions.linkUrl + "?" + params + "'>" + displayValue + "</a>"
    Mustache.to_html NAME_TEMPLATE, {
      isSticky: options.colModel.stickyCompareEnabled
      rowId: rowObject.rowId
      cssClass: options.colModel.formatoptions.style
      link: link
      export: 'export' if exportable # check if export current field
      displayValue: displayValue
      labels: options.colModel.labels
      columnName: options.colModel.columnName
    }

  showText = (value, options, rowObject) ->
    return Mustache.to_html TEXT_TEMPLATE, {
      value: value
      columnName: options.colModel.columnName
      export: 'export' if options.colModel.export
    } 

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
      value: value
      columnName: options.colModel.columnName
      confidence: confidence
      export: 'export' if options.colModel.export
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
      columnName: options.colModel.columnName
      export: 'export' if options.colModel.export
    }
    perfBar


  populationBar = (value, options, rowObject) ->
    asmt_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.results[asmt_type]

    # display empty message
    return '' if not subject
    
    # display insufficient data message
    if parseInt(value) <= 0                            
      text = options.colModel.labels['insufficient_data']
      options.colModel.columnName = subject.asmt_subject
      return showText(text, options, rowObject) 

    subject = formatSubject subject
    return Mustache.to_html POPULATION_BAR_TEMPLATE, {
      subject: subject,
      populationBar: edwarePopulationBar.create(subject)
      export: 'export' if options.colModel.export
    }


  formatExport = (value, title) ->
    #export fields
    Mustache.to_html EXPORT_TEMPLATE, {
      value: value
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
  showText: showText
  showOverallConfidence: showOverallConfidence
  showConfidence: showConfidence
  performanceBar: performanceBar
  populationBar: populationBar
