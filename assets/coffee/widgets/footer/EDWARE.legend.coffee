define [
  "jquery"
  "mustache"
  "edwareConfidenceLevelBar"
  "edwarePopulationBar"
  "edwareLOSConfidenceLevelBar"
  "text!ISRTemplate"
  "text!LOSTemplate"
  "text!CPopTemplate"
], ($, Mustache, edwareConfidenceLevelBar, edwarePopulationBar, edwareLOSConfidenceLevelBar, ISRTemplate, LOSTemplate, CPopTemplate) ->

  # Legend base class.
  # This is an abstract class, derived class should implement two functions: getTemplate() and createBar()
  class Legend

    # constructor with legend information as parameter
    constructor: (@legend) ->
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
      template = this.getTemplate()
      this.container.html Mustache.to_html(template, data)
      # create color bars
      this.createBar()

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

    getTemplate: ->
      CPopTemplate

    createBar: ->
      output = edwarePopulationBar.create this.subject
      $('#legendTemplate .populationBar', this.container).prepend(output)
      # remove pop up when hovering over population bar
      this.container.find('.progressBar_tooltip').remove()


  # Legend section on individual student report
  class ISRLegend extends Legend

    getTemplate: ->
      ISRTemplate

    createBar: ->
      # use mustache template to display the json data 
      # show 300px performance bar on html page
      output = edwareConfidenceLevelBar.create this.subject, 300
      $('#legendTemplate .losPerfBar', this.container).html(output)
      # show 640px performance bar on pdf
      output = edwareConfidenceLevelBar.create this.subject, 640
      $('#legendTemplate .confidenceLevel', this.container).html(output)

  # Legend section on list of students report
  class LOSLegend extends Legend

    getTemplate: ->
      LOSTemplate

    createBar: ->
      output = edwareLOSConfidenceLevelBar.create this.subject, 110
      $('#legendTemplate .confidenceLevel', this.container).append(output)
      # customize interval width and position
      $('.interval', this.container).css('margin-left', '89px').css('width', '28px')
      $('.indicator', this.container).css('margin-left', '98px')

  ( ($) ->

    # jQuery extension for creating legend section
    # 
    # reportName: report name, should be one of three names: 'individual_student_report', 'list_of_students', 'comparing_populations'.
    # data: contains legend info.
    $.fn.createLegend = (reportName, data) ->
      legend = undefined
      # create legend object
      if reportName is 'individual_student_report'
        legend = new ISRLegend(data)
      if reportName is 'list_of_students'
        legend = new LOSLegend(data)
      if reportName is 'comparing_populations'
        legend = new CPopLegend(data)
      # create legend section
      legend.create $(this) if legend
      $(this)
  )(jQuery)