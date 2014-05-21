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

    constructor: (@container, @contextData, @configs, @displayHome, @labels) ->
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
      if not this.displayHome
        elements.shift()
      if elements.length > 0
        elements[elements.length - 1].link = '#'
      elements

    bindEvents: ->
      items = $('li', @container)
      items.not(':last').addClass('link').hover ()->
        $this = $(this)
        $this.addClass 'active'
        $this.prev().addClass 'preceding'
      , ()->
        $this = $(this)
        $this.removeClass 'active'
        $this.prev().removeClass 'preceding'

    formatName: (element) ->
      type = element.type
      name = element.name
      if type is 'home'
        name = @labels.breadcrumb_home
      else if type is 'grade'
        name = @labels.grade + ' ' + name
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
      else if staticElement.link
        element.link = staticElement.link
      currentParams

  #
  #    *  EDWARE Breadcrumbs plugin
  #    *  @param data
  #    *  @param configs
  #    *  Example: $("#table1").breadcrumbs(data, configs)
  #
  $.fn.breadcrumbs = (contextData, configs, displayHome, labels) ->
    new EdwareBreadcrumbs(this, contextData, configs, displayHome, labels)

  #
  #    * Creates breadcrumbs widget
  #    * @param containerId - The container id for breadcrumbs
  #    * @param data
  #
  create = (containerId, contextData, configs, displayHome, labels) ->
    $(containerId).breadcrumbs contextData, configs, displayHome, labels

  create: create
  EdwareBreadcrumbs: EdwareBreadcrumbs
