define [
  'jquery'
  'mustache'
  'jqGrid'
  'edwarePopulationBar'
  'edwareConfidenceLevelBar'
  'edwareLOSConfidenceLevelBar'
  'text!edwareFormatterConfidenceTemplate'
  'text!edwareFormatterNameTemplate'
  'text!edwareFormatterPerfLevelTemplate'
  'text!edwareFormatterPerformanceBarTemplate'
  'text!edwareFormatterPopulationBarTemplate'
  'text!edwareFormatterSummaryTemplate'
  'text!edwareFormatterTextTemplate'
  'text!edwareFormatterTooltipTemplate'
  'text!edwareFormatterTotalPopulationTemplate'
  'edwarePreferences'
  'edwareContextSecurity'
], ($, Mustache, jqGrid, edwarePopulationBar, edwareConfidenceLevelBar, edwareLOSConfidenceLevelBar, edwareFormatterConfidenceTemplate, edwareFormatterNameTemplate, edwareFormatterPerfLevelTemplate, edwareFormatterPerformanceBarTemplate, edwareFormatterPopulationBarTemplate, edwareFormatterSummaryTemplate, edwareFormatterTextTemplate, edwareFormatterTooltipTemplate, edwareFormatterTotalPopulationTemplate, edwarePreferences, contextSecurity) ->

  SUMMARY_TEMPLATE = edwareFormatterSummaryTemplate

  POPULATION_BAR_TEMPLATE = edwareFormatterPopulationBarTemplate

  TOTAL_POPULATION_TEMPLATE = edwareFormatterTotalPopulationTemplate

  NAME_TEMPLATE = edwareFormatterNameTemplate

  TOOLTIP_TEMPLATE = edwareFormatterTooltipTemplate

  CONFIDENCE_TEMPLATE = edwareFormatterConfidenceTemplate

  TEXT_TEMPLATE = edwareFormatterTextTemplate

  PERFORMANCE_BAR_TEMPLATE = edwareFormatterPerformanceBarTemplate

  PERF_LEVEL_TEMPLATE = edwareFormatterPerfLevelTemplate

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
      columnName: options.colModel.label
      export: 'edwareExportColumn' if exportable
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

    buildLink = (options)->
      if contextSecurity.hasPIIAccess(rowObject.rowId)
        escaped = displayValue.replace /'/, "&#39;"
        "<a id='link_#{rowObject.rowId}' data-value='#{escaped}' href='#{options.colModel.formatoptions.linkUrl}?#{params}'>#{displayValue}</a>"
      else
        "<a class='disabled' href='#'>#{displayValue}</a>"

    # for some reason, link doesn't work well in old version of FF, have to construct manually here
    link = buildLink(options)
    Mustache.to_html NAME_TEMPLATE, {
      isSticky: options.colModel.stickyCompareEnabled
      rowId: rowObject.rowId
      cssClass: options.colModel.formatoptions.style
      link: link
      export: 'edwareExportColumn' if exportable # check if export current field
      displayValue: displayValue
      labels: options.colModel.labels
      columnName: options.colModel.label
    }

  showText = (value, options, rowObject) ->
    return Mustache.to_html TEXT_TEMPLATE, {
      value: value
      columnName: options.colModel.label
      export: 'edwareExportColumn' if options.colModel.export
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
      asmtType: subject.asmt_type,
      labels: options.colModel.labels
      value: value
      columnName: options.colModel.label
      parentName: $(options.colModel.parentLabel).text()
      confidence: confidence
      export: 'edwareExportColumn' if options.colModel.export
    }

  showPerfLevel = (value, options, rowObject) ->
    names = options.colModel.name.split "."
    subject = rowObject[names[0]]
    return '' if not subject
    perf_lvl_name = subject[names[1]][names[2]]['perf_lvl_name']
    Mustache.to_html PERF_LEVEL_TEMPLATE, {
      asmtType: subject.asmt_type,
      labels: options.colModel.labels
      perfLevelNumber: value
      columnName: options.colModel.label
      parentName: $(options.colModel.parentLabel).text()
      perfLevel: perf_lvl_name
      export: 'edwareExportColumn' if options.colModel.export
    }

  performanceBar = (value, options, rowObject) ->

    getScoreALD = (subject) ->
      return '' if not subject
      if not subject.cut_point_intervals[subject.asmt_perf_lvl-1] then "" else subject.cut_point_intervals[subject.asmt_perf_lvl-1]["name"]

    getStudentName = () ->
      name = rowObject.student_first_name if rowObject.student_first_name
      name = name + " " + rowObject.student_middle_name[0] + "." if rowObject.student_middle_name
      name = name + " " + rowObject.student_last_name if rowObject.student_last_name
      name

    getAsmtPerfLvl = (subject) ->
      return '' if not subject
      subject.asmt_perf_lvl || ''

    subject_type = options.colModel.formatoptions.asmt_type
    subject = rowObject[subject_type]
    score_ALD = getScoreALD(subject)
    student_name = getStudentName()
    asmt_perf_lvl = getAsmtPerfLvl(subject)
    rowId = rowObject.rowId + subject_type
    toolTip = Mustache.to_html TOOLTIP_TEMPLATE, {
      student_name: student_name
      subject: subject
      labels: options.colModel.labels
      score_ALD: score_ALD
      asmt_perf_lvl: asmt_perf_lvl
      confidenceLevelBar: edwareConfidenceLevelBar.create(subject, 300) if subject
      rowId: rowId
    }
    # hack to remove html tag in name
    columnName = removeHTMLTags(options.colModel.label)
    perfBar = Mustache.to_html PERFORMANCE_BAR_TEMPLATE, {
      subject: subject
      confidenceLevelBar: edwareLOSConfidenceLevelBar.create(subject, 120)  if subject
      toolTip: toolTip
      columnName: columnName
      export: 'edwareExportColumn' if options.colModel.export
      rowId: rowId
    }
    perfBar

  populationBar = (value, options, rowObject) ->
    asmt_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.results[asmt_type]

    # display empty message
    return '' if not subject
    subject = processSubject options, rowObject

    return Mustache.to_html POPULATION_BAR_TEMPLATE, {
      subject: subject
      labels: options.colModel.labels
      populationBar: edwarePopulationBar.create(subject)
      export: subject.export
      hasTextReplacement: subject.hasTextReplacement
      displayText: subject.displayText
    }

  # Used to display total population count
  totalPopulation = (value, options, rowObject) ->
    subject = processSubject options, rowObject
    return Mustache.to_html TOTAL_POPULATION_TEMPLATE, {
      subject: subject
      hasTextReplacement: subject.hasTextReplacement
      displayText: subject.displayText
      labels: options.colModel.labels
      export: subject.export
    }

  processSubject = (options, rowObject) ->
    asmt_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.results[asmt_type]
    exportable = options.colModel.export
    if subject is `undefined`
      total = 0
    else
      total = parseInt(subject.total)
    # No data when total is 0, Insufficient when total is -1
    insufficient = total < 0
    noData = total is 0
    interim = subject.hasInterim ? false
    subject.export = 'edwareExportColumn' if exportable
    subject.labels = options.colModel.labels
    subject.hasTextReplacement = insufficient || interim || noData
    if interim
      subject.displayText = options.colModel.labels['interim_data_only']
    else if insufficient
      subject.displayText = options.colModel.labels['insufficient_data']
    else if noData
      subject.displayText = options.colModel.labels['no_data_available']
    subject

  removeHTMLTags = (str) ->
    regex = ///
        <[^<|^>]+>
    ///g
    return str.replace(regex, '')

  showlink: showlink
  showText: showText
  showOverallConfidence: showOverallConfidence
  showConfidence: showConfidence
  showPerfLevel: showPerfLevel
  performanceBar: performanceBar
  populationBar: populationBar
  totalPopulation: totalPopulation
