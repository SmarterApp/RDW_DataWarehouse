define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!InfoBarTemplate"
  "edwareDownload"
], ($, bootstrap, Mustache, InfoBarTemplate, edwareDownload) ->

  POPOVER_TEMPLATE = '<div class="popover reportInfoPopover"><div class="arrow"></div><div class="popover-inner large"><div class="popover-content"><p></p></div></div></div>'

  class ReportInfoBar
  
    constructor: (@container, @config) ->
      #TODO how to specify what information expected?
      this.initialize()
      this.bindEvents()

    initialize: () ->
      $(this.container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
        subjects: @config.subjects
      this.createDownloadMenu() if not this.edwareDownloadMenu
        
    bindEvents: () ->
      self = this
      # show download menu
      $('.downloadIcon').click ->
        self.edwareDownloadMenu.show()
        
      # bind report info popover
      $('.reportInfoIcon').popover
        html: true
        placement: 'bottom'
        trigger: 'hover'
        container: '#content'
        content: @config.reportInfoText
        template: POPOVER_TEMPLATE
    
    createDownloadMenu: () ->
      this.edwareDownloadMenu = new edwareDownload.DownloadMenu($('#downloadMenuPopup'), @config)

  create = (container, config) ->
    new ReportInfoBar(container, config)

  ReportInfoBar: ReportInfoBar
  create: create