define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!InfoBarTemplate"
  "edwareDownload"
  "edwarePopover"
  "edwareDataProxy"
  "edwareSearch"
], ($, bootstrap, Mustache, InfoBarTemplate, edwareDownload, edwarePopover, edwareDataProxy, edwareSearch) ->

  class ReportInfoBar

    constructor: (@container, @config, createSearch, @contextSecurity) ->
      @initialize(createSearch)
      @bindEvent()

    initialize: (createSearch) ->
      breadcrumb = (item.name for item in @config.breadcrumb.items[1..]).join(" / ")
      $(@container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
        subjects: @config.subjects
        labels: @config.labels
        breadcrumb: breadcrumb
      @createDownloadMenu()
      @render()
      # Create search box if true, else remove it
      @searchBox ?= @createSearchBox() if createSearch

    bindEvent: () ->
      self = @
      $('.downloadIcon').click ->
        # show download menu
        self.edwareDownloadMenu.show()
      $('.reportInfoIcon').click ->
        $(this).popover('show')

    createSearchBox: () ->
      $('#search').edwareSearchBox @config.labels

    render: () ->
      # bind report info popover
      $('.reportInfoIcon').edwarePopover
        class: 'reportInfoPopover'
        labelledby: 'reportInfoPopover'
        content: @config.reportInfoText
        tabindex: 0

      # set report info text
      $('.reportInfoWrapper').append @config.reportInfoText

    createDownloadMenu: () ->
      @edwareDownloadMenu ?= new edwareDownload.DownloadMenu($('#downloadMenuPopup'), @config, @contextSecurity)

    update: () ->
      # Callback to search box to highlight if necessary
      @searchBox.addHighlight() if @searchBox

  create = (container, config, createSearch, contextSecurity) ->
    infoBar = new ReportInfoBar(container, config, createSearch, contextSecurity)

  ReportInfoBar: ReportInfoBar
  create: create
