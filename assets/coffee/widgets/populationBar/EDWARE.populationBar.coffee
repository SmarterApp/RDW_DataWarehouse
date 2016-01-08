define [
  'jquery'
  "mustache"
  "edwareUtil"
  "text!edwarePopulationBarTemplate"
], ($, Mustache, edwareUtil, populationBarTemplate) ->
  #
  #    * Population level bar widget
  #    * Generate confidence level bar and calculate cutpoint pixel width, score position, score interval position
  #
  @isPublic=edwareUtil.isPublicReport()
  $.fn.populationBar = (items) ->
    output = renderPopulationBar items
    this.html output

  renderPopulationBar = (items) ->
    rightTotalPercentage = items.sortedValue
    leftTotalPercentage = 100 - rightTotalPercentage
    if rightTotalPercentage > 0 then items.rightTotalPercentage = rightTotalPercentage
    if leftTotalPercentage > 0 then items.leftTotalPercentage = leftTotalPercentage
    items.isPublic=@isPublic
    # render population bar from template
    output = Mustache.to_html populationBarTemplate, items
    output

  create = (data, container) ->
    if container
      $(container).populationBar data
    else
      renderPopulationBar data

  create: create
