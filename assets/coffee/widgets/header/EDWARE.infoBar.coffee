###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!InfoBarTemplate"
  "edwareDownload"
  "edwarePopover"
  "edwareDataProxy"
  "edwareSearch"
  "edwareUtil"
  "edwareConstants"
  "edwarePreferences"
], ($, bootstrap, Mustache, InfoBarTemplate, edwareDownload, edwarePopover, edwareDataProxy, edwareSearch, edwareUtil, Constants, edwarePreferences) ->

  class ReportInfoBar

    constructor: (@container, @config, createSearch, @contextSecurity) ->
      @initialize(createSearch)
      @bindEvent()

    initialize: (createSearch) ->
      breadcrumb = (item.name for item in @config.breadcrumb.items[1..]).join(" / ")
      # Tenant level branding
      brandingData = edwareUtil.getTenantBrandingDataForPrint @config.metadata, false
      $(@container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
        subjects: @config.subjects
        labels: @config.labels
        breadcrumb: breadcrumb
        branding: brandingData
      @createDownloadMenu()
      @render()
      # Create search box if true, else remove it
      @searchBox ?= @createSearchBox() if createSearch

    updateAsmtTypeView: () ->
      asmtType = Constants.ASMT_TYPE[@config.param.asmtType]
      viewName = edwarePreferences.getAsmtView()
      asmtView = Constants.ASMT_VIEW[viewName?.toUpperCase()]
      subjectText =  (if asmtView isnt `undefined` then ' - ' + Constants.SUBJECT_TEXT[asmtView] else '')
      $($('.currentAsmtTypeView')[0]).html asmtType + subjectText

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
      $('.reportInfoWrapper .reportInfoText').append @config.reportInfoText

    createDownloadMenu: () ->
      @edwareDownloadMenu ?= new edwareDownload.DownloadMenu($('#downloadMenuPopup'), @config, @contextSecurity)

    update: () ->
      # Callback to search box to highlight if necessary
      @searchBox.addHighlight() if @searchBox

  create = (container, config, createSearch, contextSecurity) ->
    infoBar = new ReportInfoBar(container, config, createSearch, contextSecurity)

  ReportInfoBar: ReportInfoBar
  create: create
