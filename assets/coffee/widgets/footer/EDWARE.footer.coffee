define [
  "jquery"
  "mustache"
  "bootstrap"
  "text!edwareFooterHtml"
  "edwareLegend"
  "edwarePreferences"
  "edwareExport"
  "edwareConstants"
], ($, Mustache, bootstrap, footerTemplate, edwareLegend, edwarePreferences, edwareExport, Constants) ->

  POPOVER_TEMPLATE = '<div class="popover footerPopover {{class}}"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
  
  TITLE_TEMPLATE = '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-selector="{{selector}}">{{hide}}<img src="../images/hide_x.png"></img></i></a></div><div class="lead">{{title}}</div>'

  class EdwareFooter
  
    constructor: (@reportName, config) ->
      this.initialize(config)
      # Generate footer
      this.create()
      this.bindEvents()

    initialize: (config)->
      this.labels = config.labels
      this.reportInfo = config.reportInfo
      legendInfo = config.legendInfo
      this.legend = {
        legendInfo: legendInfo,
        subject: config.subject || (()->
          colorsData = config.colorsData
          # merge default color data into sample intervals data
          for color, i in colorsData.subject1 || colorsData.subject2
            legendInfo.sample_intervals.intervals[i].color = color
          legendInfo.sample_intervals
        )()
      }
      
    create: () ->
      $('#footer').html Mustache.to_html footerTemplate, {
        report_info: this.reportInfo
        labels: this.labels
      }
      this.createPopover()

    createPopover: () ->
      this.createFeedback()
      this.createLegend()
      this.createAbout()
      this.createHelp()
      this.createPrint()
      this.createExport()

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
        content: $(".surveyMonkeyPopup").html()

    createLegend: () ->
      # create legend
      $('.legendPopup').createLegend this.reportName, this.legend
      # create popover      
      $("#legend").popover
        html: true
        title: Mustache.to_html TITLE_TEMPLATE, {
          selector: '#legend'
          hide: this.labels.hide
          title: this.labels.legend
        }
        template: POPOVER_TEMPLATE
        content: $("#footerLinks .legendPopup").html()

    createAbout: ()->
      $("#aboutReport").popover
        html: true
        title: Mustache.to_html TITLE_TEMPLATE, {
          selector: '#aboutReport'
          hide: this.labels.hide
          title: this.labels.report_info
        }
        template: POPOVER_TEMPLATE
        content: $("#footerLinks .aboutReportPopup").html()

    createHelp: () ->
      $("#help").popover
        html: true
        title: Mustache.to_html TITLE_TEMPLATE, {
          selector: '#help'
          hide: this.labels.hide
          title: this.labels.help
        }
        template: POPOVER_TEMPLATE
        content: ->
          $(".helpPopup").html()

    createPrint: () ->
      # show "Print" only on ISR
      if this.reportName isnt Constants.REPORT_NAME.ISR
        $('#print').hide()
        return
      $("#print").popover
        html: true
        title: Mustache.to_html TITLE_TEMPLATE, {
          selector: '#print'
          hide: this.labels.hide
          title: this.labels.print_options
        }
        template: Mustache.to_html POPOVER_TEMPLATE, {
          class: 'printFooterPopover'
        }
        content: $(".printPopup").html()

    createExport: () ->
      if this.reportName is Constants.REPORT_NAME.ISR
        $('#export').hide()
        return
      $("#export").popover
        html: true
        title: Mustache.to_html TITLE_TEMPLATE, {
          selector: '#export'
          hide: this.labels.hide
          title: 'Export'
        }
        template: POPOVER_TEMPLATE
        content: $(".exportPopup").html()

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
      $(document).on 'click', '.hideButton a', ->
        selector = $(this).data('selector')
        $(selector).popover('hide')
        $("#footer .nav li a").removeClass("active")

      # bind print event
      $(document).on
        click: ->
          val=$('input[name=print_options]:checked').val()
          asmtType = $('#selectedAsmtType').text()
          url=document.URL.replace("indivStudentReport","print")
          url += '&pdf=true'
          if val is "gray"
            url += "&grayscale=true"
          if asmtType
             url += "&asmtType=" + encodeURI asmtType
          url += "&lang=" + edwarePreferences.getSelectedLanguage()
          $("#print").popover "hide"
          $("#footer .nav li a").removeClass("active")
          window.open(url, "_blank",'toolbar=0,location=0,menubar=0,status=0,resizable=yes')
        , "#printButton"

      # bind export event
      $(document).on 'click', '#exportButton', ->
        $('#gridTable').edwareExport self.reportName


  EdwareFooter: EdwareFooter