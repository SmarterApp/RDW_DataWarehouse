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
  "text!YearDropdownTemplate"
  "edwarePreferences"
  "edwareEvents"
], ($, Mustache, YearDropdownTemplate, edwarePreferences, edwareEvents) ->

  class AcademicYearDropdown

    constructor: (@container, @years, @callback) ->
      @initialize()
      @setDefaultOption()
      @bindEvents()

    initialize: () ->
      return if not @years
      @latestYear = @years[0].value
      output = Mustache.to_html YearDropdownTemplate,
        options: @years
      $(@container).html output
      # set latest year to reminder message
      $('.latestYear', ".reminderMessage").html @years[0].display

    setDefaultOption: () ->
      asmtYear = edwarePreferences.getAsmtYearPreference()
      if not asmtYear
        asmtYear = @years[0].value
        edwarePreferences.saveAsmtYearPreference(asmtYear)
      display = (asmtYear - 1) + " - " + asmtYear
      @setSelectedValue display, asmtYear

    setSelectedValue: (display, value) ->
      $(".selectedAcademicYear").html(display)
      $reminder =  $(".reminderMessage")
      if not value || value is @latestYear
        $reminder.hide()
      else
        $reminder.show()

    bindEvents: () ->
      self = this
      $(@container).onClickAndEnterKey 'li', ->
        display = $(this).data('display')
        value = $(this).data('value')
        self.setSelectedValue display, value
        edwarePreferences.saveAsmtYearPreference(value)
        # TODO: move focus on button after selection
        $('#academicYearAnchor button').focus()
        self.callback(value)

      # hide on focus lost
      @container.focuslost ()->
        self.hide()

      $('.reminderMessage a').unbind('click').click ->
        value = self.latestYear
        edwarePreferences.saveAsmtYearPreference(value)
        self.callback(value)

    hide: ()->
      @container.find('.btn-group').removeClass('open')


  (($) ->
    $.fn.createYearDropdown = (options, callback)->
      new AcademicYearDropdown(this, options, callback)
  ) jQuery

  AcademicYearDropdown: AcademicYearDropdown
