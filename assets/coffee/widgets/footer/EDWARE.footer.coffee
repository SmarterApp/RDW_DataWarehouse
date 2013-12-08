define [
  "jquery"
  "mustache"
  "bootstrap"
  "text!edwareFooterHtml"
  "edwarePreferences"
  "edwareExport"
  "edwareConstants"
  "edwareClientStorage"
  "edwareHelpMenu"
], ($, Mustache, bootstrap, footerTemplate, edwarePreferences, edwareExport, Constants, edwareClientStorage, edwareHelpMenu) ->

  POPOVER_TEMPLATE = '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'

  TITLE_TEMPLATE = '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-selector="{{selector}}">{{hide}}<img src="../images/hide_x.png"></img></i></a></div><div class="lead">{{title}}</div>'

  class EdwareFooter

    constructor: (@reportName, config, @reportType) ->
      this.initialize(config)
      this.create()
      this.bindEvents()

    initialize: (config)->
      this.labels = config.labels

    create: (config) ->
      $('#footer').html Mustache.to_html footerTemplate, {
        labels: this.labels
      }
      # create popover
      this.createPopover()

    createPopover: () ->
      this.createFeedback()
      this.createHelp()

    createFeedback: () ->
      # Survey monkey popup
      $("#feedback").popover
        html: true
        title: Mustache.to_html TITLE_TEMPLATE, {
          selector: '#feedback'
          hide: this.labels.hide
          title: this.labels.feedback
        }
        template: POPOVER_TEMPLATE
        content: () ->
          $(".surveyMonkeyPopup").html()

    createHelp: () ->
      @helpMenu ?= edwareHelpMenu.create '.HelpMenuContainer',
        labels: this.labels

    bindEvents: ()->
      self = this
      # Make the footer button active when associate popup opens up
      $('#footer .nav li a').click ->
        $("#footer .nav li a").not($(this)).each ->
          $this = $(this)
          $this.removeClass("active")
          $('#' + $this.attr('id')).popover('hide')
        $(this).toggleClass("active")

      # Popup will close if user clicks popup hide button
      $(document).on 'click', '#help', ->
        self.helpMenu.show()
        

  EdwareFooter: EdwareFooter
