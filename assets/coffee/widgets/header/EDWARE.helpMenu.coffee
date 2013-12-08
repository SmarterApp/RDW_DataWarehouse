define [
  "jquery"
  "mustache"
  "text!HelpMenuTemplate"
], ($, Mustache, HelpMenuTemplate) ->

  class EdwareHelpMenu
    
    constructor: (@container, @config) ->
      @initialize()
      @bindEvents()
            
    initialize: () ->
      output = Mustache.to_html HelpMenuTemplate, @config
      $(@container).html(output)

    bindEvents: () ->
      $('#helpMenuTab a').click (e) ->
        e.preventDefault()
        $(this).tab 'show'
      
    show: () ->
      $('#HelpMenuModal').modal 'show'

  create = (container, config) ->
    new EdwareHelpMenu(container, config)

  EdwareHelpMenu: EdwareHelpMenu
  create: create
