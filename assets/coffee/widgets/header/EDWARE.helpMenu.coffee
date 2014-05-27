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
      self = this
      tabs = $('#helpMenuTab')
      # stop from triggering modal show event, such that last focused
      # element won't be reset
      tabs.find('a').on 'show', (e) ->
        e.stopPropagation()
      # show selected tab
      tabs.find('a').click (e) ->
        e.preventDefault()
        $this = $(this)
        self.setActiveTabId $this.attr('href')
        $this.tab 'show'
      # show tab when menu modal dropdown, if any
      $('#HelpMenuModal').on 'shown', ->
        if self.activeTab
          target = tabs.find("a[href='" + self.activeTab + "']")
        else
          target = tabs.find("a:first")
        target.tab 'show'

    setActiveTabId: (tabId) ->
      @activeTab = tabId

    show: (tabId) ->
      @setActiveTabId tabId if tabId
      $('#HelpMenuModal').edwareModal()


  create = (container, config) ->
    new EdwareHelpMenu(container, config)

  EdwareHelpMenu: EdwareHelpMenu
  create: create
