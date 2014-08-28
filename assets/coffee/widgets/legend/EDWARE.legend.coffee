define [
  "jquery"
  "mustache"
  "edwareDataProxy"
  "edwareConfidenceLevelBar"
  "edwarePopulationBar"
  "edwareLOSConfidenceLevelBar"
  "text!ISRTemplate"
  "text!LOSTemplate"
  "text!CPopTemplate"
  "edwareConstants"
  "edwarePopover"
], ($, Mustache, edwareDataProxy, edwareConfidenceLevelBar, edwarePopulationBar, edwareLOSConfidenceLevelBar, ISRTemplate, LOSTemplate, CPopTemplate, Constants, edwarePopover) ->

  # Legend base class.
  # This is an abstract class, derived class should implement two functions: getTemplate() and createBar()
  class Legend

    # constructor with legend information as parameter
    constructor: (@legend, @reportName) ->
      this.subject = this.legend['subject']

    # create legend in html format from mustache template
    create: (@container) ->
      data = {}
      # create ALD intervals
      data['ALDs'] = this.createALDs this.subject
      # text from json file
      data['legendInfo'] = this.legend['legendInfo']
      # need assessment score and color to display legend consistently across all ISR
      data['asmtScore'] = this.legend['subject'].asmt_score
      data['scoreColor'] = this.legend['subject'].score_color

      data.labels = this.legend.labels
      @container.html Mustache.to_html(@getTemplate(), data)
      # create color bars
      @createBar(@subject, @container)


    # get template of legend section
    getTemplate: ->
      ""

    # create custom color bars
    createBar: ->
      ""

    # create ALDs table
    createALDs: (items) ->
      # create intervals to display on ALD table
      ALDs = []
      intervals = items.cut_point_intervals
      i = 0
      while i < intervals.length
        interval = {}
        interval['color'] = intervals[i]['bg_color']
        interval['description'] = intervals[i]['name']
        start_score = if i == 0 then items.asmt_score_min else intervals[i-1]['interval']
        end_score = if i == intervals.length - 1 then items.asmt_score_max else (intervals[i]['interval'] - 1)
        interval['range'] = start_score + '-' + end_score
        ALDs.push interval
        i++
      ALDs


  # Legend section on comparing population report
  class CPopLegend extends Legend

    constructor: (@legend) ->
      super legend, 'comparingPopulationsReport'

    getTemplate: ->
      CPopTemplate

    createBar:(subject, container) ->
      output = edwarePopulationBar.create subject
      $('#legendTemplate .populationBar', container).prepend(output)
      $('#legendTemplate .populationBarSmall', container).prepend(output)
      # do not tab on progress bar in legend
      container.find('.progress').removeAttr('tabindex')
      # Show tooltip for population bar on mouseover
      $("#legendTemplate .populationBarSmall .progress").edwarePopover
        class: 'legendAchievementLevel'
        html: true
        placement: 'top'
        container: '#legendTemplate .populationBarSmallTooltip'
        trigger: 'manual'
        content: ->
          # template location: widgets/populationBar/template.html
          $(this).find(".progressBar_tooltip").html()
      $("#legendTemplate .populationBarSmall .progress").popover('show')

  # Legend section on individual student report
  class ISRLegend extends Legend

    constructor: (@legend) ->
      super legend, 'indivStudentReport'

    getTemplate: ->
      ISRTemplate

    createBar: (subject, container)->
      # use mustache template to display the json data
      # show 300px performance bar on html page
      output = edwareConfidenceLevelBar.create subject, 640
      $('#legendTemplate .isrPerfBar', container).html(output)
      # show small performance bar on html page
      output = edwareConfidenceLevelBar.create subject, 198
      $('#legendTemplate .isrBarDetails .isrPerfBarSmall', container).html(output)
      # show 640px performance bar on pdf
      output = edwareConfidenceLevelBar.create subject, 640
      $('#legendTemplatePrint .confidenceLevel', container).html(output)

  # Legend section on list of students report
  class LOSLegend extends Legend

    constructor: (@legend) ->
      super legend, 'studentList'

    getTemplate: ->
      LOSTemplate

    createBar: (subject, container)->
      # confidence level bar
      output = edwareLOSConfidenceLevelBar.create subject, 180
      $('#legendTemplate .confidenceLevel', container).append(output)
      # error band
      $('#legendTemplate .errorBand', container).append(output)

  ( ($) ->

    # jQuery extension for creating legend section
    #
    # reportName: report name, should be one of three names: 'individual_student_report', 'list_of_students', 'comparing_populations'.
    # data: contains legend info.
    $.fn.createLegend = (reportName, data) ->
      legend = undefined
      # create legend object
      if reportName is Constants.REPORT_NAME.ISR
        legend = new ISRLegend(data)
      if reportName is Constants.REPORT_NAME.LOS
        legend = new LOSLegend(data)
      if reportName is Constants.REPORT_NAME.CPOP
        legend = new CPopLegend(data)
      # create legend section
      legend.create $(this) if legend
      $(this)
  )(jQuery)
