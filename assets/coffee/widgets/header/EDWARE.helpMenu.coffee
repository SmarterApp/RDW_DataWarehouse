define [
  "jquery"
  "mustache"
  "edwareDataProxy"
  "text!HelpMenuTemplate"
], ($, Mustache, edwareDataProxy, HelpMenuTemplate) ->

  class EdwareHelpMenu

    constructor: (@container, @config) ->
      self = this
      edwareDataProxy.getDataForHelpContent().done (data) ->
        self.data = data
        self.initialize()
        self.bindEvents()

    initialize: () ->
      output = Mustache.to_html HelpMenuTemplate, {
          labels: @config.labels
          helpContent: @data
      } 
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
      $(window).resize (e) ->
        self.setModalSize()

    setActiveTabId: (tabId) ->
      @activeTab = tabId

    show: (tabId) ->
      @setActiveTabId tabId if tabId
      $('#HelpMenuModal').edwareModal()
      this.setModalSize()
    
    setModalSize: () ->
      # Adjust the modal height based on window height
      windowHeight = $(window).height()
      # This is an approximate height for content area in help modal
      height = windowHeight - 210
      if height < 0
        height = 1
      mainModal = $('#HelpMenuModal')
      content = $('#HelpMenuModal .tab-content')
      mainModal.css('top', '30px')
      mainModal.css('height', height + 80 + 'px')
      content.css('height', height + 'px')
      content.css('max-height', height + 'px')
  

  create = (container, config) ->
    new EdwareHelpMenu(container, config)

  EdwareHelpMenu: EdwareHelpMenu
  create: create
