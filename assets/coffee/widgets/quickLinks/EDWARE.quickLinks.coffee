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
      @dataRows = @processData()
      @initialize()
      @setDefaultOptions()
      @bindEvents()

    initialize: () ->
      # Up to 4 per row
      # districtRows = [ { districts: [ { type : x, id: x, items: [{display: x, link: y }], className: y, showMore: true, showMoreText: 'more' } } ]
      output = Mustache.to_html quickLinksTemplate,
        districtRows: @dataRows.districts
        isDistricts: @dataRows.districts.length > 0
        schoolRows: @dataRows.schools
        isSchools: @dataRows.schools.length > 0
      @container.html(output)

    setDefaultOptions: () ->
      # Set quicklink display state
      state = edwarePreferences.getQuickLinksState()
      # Set to open if not in prefs
      state = true if state is undefined
      @setViewOption state

    # Set elements to states
    setViewOption: (state) ->
      @toggle '#quickLinks_data', state
      @toggle '#quickLinks_link', !state

    # Process data
    processData: () ->
      output = {}
      for key, list of @data
        output[key] ?= []
        items = []
        i = 0
        for item, index in list
          link = 'comparingPopulations.html?stateCode=' + item.params.stateCode + '&districtId=' + item.params.districtId
          link += '&schoolId=' + item.params.schoolId if item.params.schoolId
          i = index
          items.push
            display: item.name
            link: link
        item =
          items : items
          type : key
          id : i
          className: 'more'
          showMore: items.length >= 4,
          showMoreText: 'more'
        output[key].push(item)
      output

    # Assign a class to an el
    toggle: (el, state) ->
      className = if state then 'open' else "close"
      $(el).attr('class', className)

    bindEvents: () ->
      self = this
      $('#quickLinks_close').click ->
        # Toggle
        self.setViewOption false
        # Save prefs
        edwarePreferences.saveQuickLinksState false

      $('#quickLinks_open').click ->
        # Toggle
        self.setViewOption true
        # Save prefs
        edwarePreferences.saveQuickLinksState true

      $('.quickLinks_expand').click ->
        type = $(this).data('type')
        id = $(this).data('id')+1
        # check current status
        isOpen = if $(this).html()=='more' then 'more' else 'less'
        # change the class/copy
        update = if isOpen=='more' then 'less' else 'more'
        $(this).html(update)
        # change el
        $('#'+type+'_'+id).attr('class', update)

  (($)->
    $.fn.createEdwareQuickLinks = (data) ->
      new EdwareQuickLinks(@, data)
  ) jQuery

  EdwareQuickLinks: EdwareQuickLinks
