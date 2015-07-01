define [
  "jquery"
  "mustache"
  "text!quickLinksTemplate"
  "edwarePreferences"
  "edwareEvents"
  "edwareConstants"
], ($, Mustache, quickLinksTemplate, edwarePreferences, edwareEvents, Constants) ->

  class EdwareQuickLinks

    constructor: (@container, @data) ->
      @initialize()
      @setDefaultOption()
      @bindEvents()

    initialize: () ->
      output = Mustache.to_html quickLinksTemplate,
        districts: @processData @data.districts
        schools: @processData @data.schools
      @container.html(output)

    setDefaultOption: () ->
      state = edwarePreferences.getQuickLinksState()
      # Set to open if not in prefs
      state = true if state is undefined
      @setOption state

    # Set elements to states
    setOption: (state) ->
      @toggle '#quickLinks_data', state
      @toggle '#quickLinks_link', !state

    # Process data 
    processData: (data) ->
      output = []
      for item in data
        link = 'comparingPopulations.html?stateCode=' + item.params.stateCode + '&districtId=' + item.params.districtId
        link += '&schoolId=' + item.params.schoolId if item.params.schoolId
        output.push
          display: item.name
          link: link
      output

    # Assign a class to an el
    toggle: (el, state) ->
      className = if state then 'open' else "close"
      $(el).attr('class', className)

    bindEvents: () ->
      self = this
      $('#quickLinks_close').click ->
        # Toggle
        self.setOption false
        # Save prefs
        edwarePreferences.saveQuickLinksState false

      $('#quickLinks_open').click ->
        # Toggle
        self.setOption true
        # Save prefs
        edwarePreferences.saveQuickLinksState true

  (($)->
    $.fn.createEdwareQuickLinks = (data) ->
      new EdwareQuickLinks(@, data)
  ) jQuery

  EdwareQuickLinks: EdwareQuickLinks
