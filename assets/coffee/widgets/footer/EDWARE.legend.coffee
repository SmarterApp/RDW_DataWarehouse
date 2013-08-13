define [
  "jquery"
  "mustache"
  "edwareConfidenceLevelBar"
  "edwarePopulationBar"
<<<<<<< Updated upstream
  "text!ISRTemplate"
  "text!LOSTemplate"
  "text!CPopTemplate"
], ($, Mustache, edwareConfidenceLevelBar, edwarePopulationBar, ISRTemplate, LOSTemplate, CPopTemplate) ->
=======
  "edwareLOSConfidenceLevelBar"
  "text!ISRTemplate"
  "text!LOSTemplate"
  "text!CPopTemplate"
], ($, Mustache, edwareConfidenceLevelBar, edwarePopulationBar, edwareLOSConfidenceLevelBar, ISRTemplate, LOSTemplate, CPopTemplate) ->
>>>>>>> Stashed changes

  class Legend

    constructor: (@legend) ->
      this.subject = this.legend['subject']

    create: (@container) ->
      # create legend in html format from mustache template
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

    getTemplate: ->
      ""

    createBar: ->
      ""

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


  class CPopLegend extends Legend

    getTemplate: ->
      CPopTemplate

    createBar: ->
      output = edwarePopulationBar.create this.subject
<<<<<<< Updated upstream
      $('#legendTemplate .populationBar', this.container).html(output)
=======
      $('#legendTemplate .populationBar', this.container).prepend(output)
>>>>>>> Stashed changes
      # remove pop up when hovering over population bar
      this.container.find('.progressBar_tooltip').remove()


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

  class LOSLegend extends Legend

    getTemplate: ->
      LOSTemplate

<<<<<<< Updated upstream
=======
    createBar: ->
      output = edwareLOSConfidenceLevelBar.create this.subject, 150
      $('#legendTemplate .confidenceLevel', this.container).html(output)


>>>>>>> Stashed changes

  ( ($) ->
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