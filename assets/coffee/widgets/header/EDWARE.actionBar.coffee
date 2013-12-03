define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!ActionBarTemplate"
  "edwareDownload"
], ($, bootstrap, Mustache, ActionBarTemplate, edwareDownload) ->

  class ReportActionBar
  
    constructor: (@container, @config) ->
      this.initialize()
      this.bindEvents()

    initialize: () ->
      $(this.container).html Mustache.to_html ActionBarTemplate,
        labels: @config.labels
                
    bindEvents: () ->
      self = this


  create = (container, config) ->
    new ReportActionBar(container, config)

  ReportActionBar: ReportActionBar
  create: create