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
  "edwarePreferences"
  "edwarePopover"
  "edwareConstants"
], ($, Mustache, edwarePreferences, edwarePopover, Constants) ->


  class EdwareDisclaimer

    constructor: (@content) ->
      @interimDisclaimerIcon = $('.interimDisclaimerIcon')
      @bindEvents()
      @

    displayPopover: ()->
      unless @hasLoaded()
        self = this
        # make popup and make it stay
        @interimDisclaimerIcon.popover 'show'
        setTimeout (->
          self.interimDisclaimerIcon.popover 'hide'
        ), 10000
        # This will save that we've loaded it the first time
        @saveLoadedInfo()

    bindEvents: () ->
      self = this
      # Show tooltip on mouseover
      @interimDisclaimerIcon.edwarePopover
        class: 'disclaimerPopover'
        content: @content
        tabindex: 0
      .click ->
        $(this).mouseover()

    hasLoaded: () ->
      edwarePreferences.getInterimInfo()

    saveLoadedInfo: () ->
      edwarePreferences.saveInterimInfo()

    update: (asmt) ->
      if (typeof asmt is 'string') and (asmt.toUpperCase() in [Constants.ASMT_TYPE['INTERIM COMPREHENSIVE'].toUpperCase(), Constants.ASMT_TYPE['INTERIM ASSESSMENT BLOCKS'].toUpperCase()])
        @interimDisclaimerIcon.show()
        @displayPopover()
        # show on print version
        $('.disclaimerInfo.printContent').append(@content)
      else
        @interimDisclaimerIcon.hide()
        $('.disclaimerInfo.printContent').empty()

  (($)->
    $.fn.edwareDisclaimer = (content) ->
      new EdwareDisclaimer(content)
  ) jQuery
