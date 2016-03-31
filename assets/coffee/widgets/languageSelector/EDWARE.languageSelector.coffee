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
  "edwareDataProxy"
  "edwarePreferences"
],($, edwareDataProxy, edwarePreferences) ->

  create = (language_selector, labels) ->
    language_selector.prepend $("""
      <div class='language_selections_header' aria-hidden='true'>
        <div class='padTopBottom9'><i class='icon-globe'></i>#{labels.language}</div>
          <li class='divider' role='radio'></li>
      </div>
      <div class='language_selections_body padTopBottom9'></div>
      """)
    language_selector_body = language_selector.find('.language_selections_body')
    current_lang = edwarePreferences.getSelectedLanguage()
    loadingLanguage = edwareDataProxy.getDatafromSource "../data/languages.json"
    loadingLanguage.done (data)->
      languages = data['languages']

      $.each languages, (lang, name) ->
        language_selections = $('<li></li>')
        input = $("<input type='radio' name='language' value='#{lang}' aria-label='#{name}'>
          <span aria-hidden='true'>#{name}</span></input>")
        if lang is current_lang
          input.attr('checked', true)
          $('#user-settings span.lang').text name
          $('.headerLink .selectedLanguage').text name
        language_selections.append input
        language_selector_body.append language_selections

      radioButtons = $('input[name="language"]:radio')
      radioButtons.mouseup (e)->
        lang_id = $(this).attr "value"
        language_name = $('#' + lang_id).text()
        edwarePreferences.saveSelectedLanguage lang_id
        location.reload() unless current_lang is lang_id
      .keypress (e) ->
        if e.keyCode is 13
          $(this).mouseup()
      .on 'click', (e)->
        # keep language dropdown menu open
        e.stopPropagation()
    $('#languageSelector').focuslost ->
      $(this).mouseleave()
  create: create
