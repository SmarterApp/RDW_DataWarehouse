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
  'text!edwareFormatterStatusTemplate'
  'text!edwareFormatterTextTemplate'
  'text!edwareFormatterTooltipTemplate'
  'text!edwareFormatterTotalPopulationTemplate'
  'edwarePreferences'
  'edwareContextSecurity'
  'edwareConstants'
  'edwareUtil'
], ($, Mustache, jqGrid, edwarePopulationBar, edwareConfidenceLevelBar, edwareLOSConfidenceLevelBar, edwareFormatterConfidenceTemplate, edwareFormatterNameTemplate, edwareFormatterPerfLevelTemplate, edwareFormatterPerformanceBarTemplate, edwareFormatterPopulationBarTemplate, edwareFormatterSummaryTemplate, edwareFormatterStatusTemplate, edwareFormatterTextTemplate, edwareFormatterTooltipTemplate, edwareFormatterTotalPopulationTemplate, edwarePreferences, contextSecurity, Constants, edwareUtil) ->

  SUMMARY_TEMPLATE = edwareFormatterSummaryTemplate

  STATUS_TEMPLATE = edwareFormatterStatusTemplate

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

  showStatus = (value, options, rowObject) ->
    return Mustache.to_html STATUS_TEMPLATE, {
        cssClass: options.colModel.formatoptions.style
        subTitle: rowObject.subtitle
        value: value
    }

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
    asmt_subject_text = Constants.SUBJECT_TEXT[subject.asmt_type]
    perf_lvl_name = subject[names[1]][names[2]]['perf_lvl_name']
    Mustache.to_html PERF_LEVEL_TEMPLATE, {
      asmtType: subject.asmt_type,
      asmtSubjectText: asmt_subject_text
      labels: options.colModel.labels
      perfLevelNumber: value
      columnName: options.colModel.label
      parentName: $(options.colModel.parentLabel).text()
      perfLevel: perf_lvl_name
      export: 'edwareExportColumn' if options.colModel.export
    }

  showPerfLevelIAB = (value, options, rowObject) ->
    names = options.colModel.name.split "."
    subject = rowObject[names[0]]
    return '' if not subject
    asmt_subject_text = Constants.SUBJECT_TEXT[subject.asmt_type]
    columnData = subject[names[1]]
    date_taken = names[2]
    labels = options.colModel.labels

    perf_lvl_name = ""
    if columnData
      #Loop backwards as collapsed columns use the last perf_lvl_name
      for i in [columnData.length - 1..0] by -1
        data = columnData[i]
        date = data.date_taken
        data.display_date_taken = edwareUtil.formatDate(date)
        if date is date_taken or date_taken == labels['latest_result']
          perf_lvl_name = data[names[3]][names[4]]['perf_lvl_name']
          value = data[names[3]][names[4]]['perf_lvl']

    isExpanded = options.colModel.expanded
    dateText = { text: if isExpanded then date_taken else labels['latest_result'] }
    Mustache.to_html PERF_LEVEL_TEMPLATE, {
      displayPopover: not options.colModel.expanded  # Only show popover when not expanded
      oldResultsClass: if not isExpanded then "hasOlderResults" else ""
      student_full_name: rowObject.student_full_name
      student_full_name_date_taken: rowObject.student_full_name_date_taken
      prev: columnData
      asmtType: subject.asmt_type,
      asmtSubjectText: asmt_subject_text
      labels: labels
      perfLevelNumber: value
      columnName: options.colModel.label
      parentName: $(options.colModel.parentLabel).text()
      perfLevel: perf_lvl_name
      dateTakenText: dateText
      export: 'edwareExportColumn' if options.colModel.export
    }

  performanceBar = (value, options, rowObject) ->

    getScoreALD = (subject) ->
      return '' if not subject
      if not subject.asmt_perf_lvl then "" else options.colModel.labels.asmt.perf_lvl_name[subject.asmt_perf_lvl]

    getStudentName = () ->
      name = rowObject.student_first_name if rowObject.student_first_name
      name = name + " " + rowObject.student_middle_name[0] + "." if rowObject.student_middle_name
      name = name + " " + rowObject.student_last_name if rowObject.student_last_name
      name

    getAsmtPerfLvl = (subject) ->
      return '' if not subject
      subject.asmt_perf_lvl || ''

    getSubjectText = (subject) ->
      return '' if not subject
      Constants.SUBJECT_TEXT[subject.asmt_type]

    subject_type = options.colModel.formatoptions.asmt_type
    subject = rowObject[subject_type]
    score_ALD = getScoreALD(subject)
    asmt_subject_text = getSubjectText(subject)
    student_name = getStudentName()
    asmt_perf_lvl = getAsmtPerfLvl(subject)
    rowId = rowObject.rowId + subject_type
    toolTip = Mustache.to_html TOOLTIP_TEMPLATE, {
      student_name: student_name
      asmt_subject_text: asmt_subject_text
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
      asmt_subject_text: asmt_subject_text
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
      header: rowObject.header
    }

  # Used to display total population count
  totalPopulation = (value, options, rowObject) ->
    subject = processSubject options, rowObject
    unfilter_msg = Mustache.to_html options.colModel.labels.out_of_students, {count: subject.unfilteredTotal}
    return Mustache.to_html TOTAL_POPULATION_TEMPLATE, {
      subject: subject
      hasTextReplacement: subject.hasTextReplacement
      displayText: subject.displayText
      labels: options.colModel.labels
      export: subject.export
      unfilter_msg: unfilter_msg
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
      subject.summative = false
    else if insufficient
      subject.displayText = options.colModel.labels['insufficient_data']
      subject.summative = false
    else if noData
      subject.displayText = options.colModel.labels['no_data_available']
      subject.summative = false
    else
      subject.summative = true
    subject.asmt_subject_text = Constants.SUBJECT_TEXT[subject.asmt_subject]
    subject

  removeHTMLTags = (str) ->
    regex = ///
        <[^<|^>]+>
    ///g
    return str.replace(regex, '')

  showlink: showlink
  showText: showText
  showStatus: showStatus
  showOverallConfidence: showOverallConfidence
  showConfidence: showConfidence
  showPerfLevel: showPerfLevel
  showPerfLevelIAB: showPerfLevelIAB
  performanceBar: performanceBar
  populationBar: populationBar
  totalPopulation: totalPopulation
