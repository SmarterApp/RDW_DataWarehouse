define [
  "jquery"
  "mustache"
  "text!quickLinksTemplate"
  "edwarePreferences"
  "edwareDataProxy"
  "edwareEvents"
  "edwareConstants"
], ($, Mustache, quickLinksTemplate, edwarePreferences, edwareDataProxy, edwareEvents, Constants) ->

  class EdwareQuickLinks

    SHOW_NEXT_ROW =
      MORE: 'more'
      LESS: 'less'

    constructor: (@container) ->
      @initialize()

    initialize: () ->
      self = this
      params = stateCode: edwarePreferences.getStateCode()

      loadingData = this.fetchData params
      loadingData.done((data) ->
        self.dataRows = self.processData(data.quick_links)
        output = Mustache.to_html quickLinksTemplate,
            districtRows: self.dataRows.districts
            isDistricts: self.dataRows.districts.length > 0
            schoolRows: self.dataRows.schools
            isSchools: self.dataRows.schools.length > 0
        self.container.html(output)
        self.setDefaultOptions()
        self.bindEvents()
      )

    setDefaultOptions: () ->
      # Set quicklink display state
      state = edwarePreferences.getQuickLinksState()
      # Set to open if not in prefs
      state = true if state is undefined
      @setViewOption state

    fetchData: (params)->
      options =
        method: "POST"
        params: params

      edwareDataProxy.getDatafromSource "/data/quick_links", options

    # Set elements to states
    setViewOption: (state) ->
      @toggle '#quickLinks_data', state
      @toggle '#quickLinks_link', !state

    # Process data
    processData: (data) ->
      output = {}
      for key, list of data
        output[key] ?= []
        # Spit list in groups of 4
        splitItems = (list.splice(0, 4) while list.length)
        # Build rows with 4 items per row
        # with unique type-id for div id
        for group, groupIndex in splitItems
          items = []
          for item, index in group
            link = 'comparingPopulations.html?stateCode=' + item.params.stateCode + '&districtId=' + item.params.districtId
            link += '&schoolId=' + item.params.schoolId if item.params.schoolId
            items.push
              display: item.name
              link: link
          item =
            items : items
            type : key
            id : groupIndex
            # Always show the 1st row
            className: if groupIndex is 0 then SHOW_NEXT_ROW.MORE else SHOW_NEXT_ROW.LESS
            # Display more/less in case of additional items
            showNextRow: splitItems[groupIndex+1] isnt undefined
            # Display more/less text in case of additional items
            showNextRowText: if splitItems[groupIndex+1] then SHOW_NEXT_ROW.MORE else SHOW_NEXT_ROW.LESS
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
        el = $(this)
        type = el.data('type')
        # Next row id
        id = el.data('id')+1
        copy = el.find('.copy').html()
        # Check current class
        rowClass = if copy == SHOW_NEXT_ROW.MORE then SHOW_NEXT_ROW.MORE else SHOW_NEXT_ROW.LESS
        # Reverse copy
        linkCopy = if copy == SHOW_NEXT_ROW.MORE then SHOW_NEXT_ROW.LESS else SHOW_NEXT_ROW.MORE
        # Update el
        el.empty()
        $('<span class="copy">'+linkCopy+'</span><span class="'+linkCopy+'"></span>').appendTo(el)
        # Change row class
        $('#'+type+'_'+id).attr('class', rowClass)

  (($)->
    $.fn.createEdwareQuickLinks = () ->
      new EdwareQuickLinks(@)
  ) jQuery

  EdwareQuickLinks: EdwareQuickLinks
