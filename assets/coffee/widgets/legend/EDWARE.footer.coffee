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
  "mustache"
  "bootstrap"
  "text!edwareFooterHtml"
  "edwarePreferences"
  "edwareExport"
  "edwareConstants"
  "edwareClientStorage"
], ($, Mustache, bootstrap, footerTemplate, edwarePreferences, edwareExport, Constants, edwareClientStorage) ->

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
        

  EdwareFooter: EdwareFooter
