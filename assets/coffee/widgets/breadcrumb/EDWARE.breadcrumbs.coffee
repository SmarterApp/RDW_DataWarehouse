#
# * EDWARE breadcrumbs
# * The module contains EDWARE breadcrumbs plugin and breadcrumbs creation method
#
define [
  'jquery'
  "mustache"
  "edwareDataProxy"
] , ($, Mustache, edwareDataProxy) ->

  BREADCRUMBS_TEMPLATE = "<ul>{{#items}}<li><a href='{{link}}'>{{name}}</a></li>{{/items}}<ul>"

  class EdwareBreadcrumbs

    constructor: (@container, @contextData, @configs) ->
      @initialize()
      @bindEvents()

    initialize: ->
      elements = @getCurrentPath()
      output = Mustache.to_html BREADCRUMBS_TEMPLATE,
        items: elements
      $(@container).html output

    getCurrentPath: ->
      elements = []
      for element, i in @contextData['items']
        staticElement = @configs['items'][i]
        if staticElement.type isnt element.type
          # make sure the type matches with the type from json file          
          continue
        # sets the url link and returns the current query parameters
        currentParams = @setUrlLink currentParams, element, staticElement
        elements.push @formatName element
      elements[elements.length - 1].link = '#'
      elements

    bindEvents: ->
      items = $('li', @container)
      items.not(':last').addClass('link').hover ()->
        $this = $(this)
        $this.addClass 'focus'
        $this.prev().addClass 'active'
      , ()->
        $this = $(this)
        $this.removeClass 'focus'
        $this.prev().removeClass 'active'

    formatName: (element) ->
      type = element.type
      name = element.name
      if type is 'grade'
        name = "Grade " + name
      else if type is 'student'
        # Special case for names that end with an 's'
        name += if /s$|S$/.test(name) then "'" else "'s"
        name += " Results"
      element.name = name
      element

    setUrlLink: (currentParams, element, staticElement) ->
      # Appends the current set of query parameters to build breadcrumb link
      # Sets element.link used for individual breadcrumb links
      # currentParams keeps track of existing query parameters for the rest of the breadcrumb trail
      currentParams ?= ''
      if element.id
        params = staticElement.queryParam + "=" + element.id
        if currentParams.length is 0
          currentParams = params
        else
          currentParams = currentParams + "&" + params
        element.link = staticElement.link + "?" + currentParams
      currentParams

  #
  #    *  EDWARE Breadcrumbs plugin
  #    *  @param data
  #    *  @param configs
  #    *  Example: $("#table1").breadcrumbs(data, configs)
  #
  $.fn.breadcrumbs = (contextData, configs) ->
    new EdwareBreadcrumbs(this, contextData, configs)
    
  #
  #    * Creates breadcrumbs widget
  #    * @param containerId - The container id for breadcrumbs
  #    * @param data
  #
  create = (containerId, contextData, configs) ->
    $(containerId).breadcrumbs contextData, configs

  create: create
  EdwareBreadcrumbs: EdwareBreadcrumbs
