define [
  "jquery"
  "edwareDataProxy"
  "edwarePreferences"
],($, edwareDataProxy, edwarePreferences) ->

  create = (language_selector, labels) ->
    language_selector.prepend $("""
      <div class='language_selections_header'>
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
        input = $("<input type='radio' name='language' value='#{lang}'>#{name}</input>")
        if lang is current_lang
          input.attr('checked', true)
          $('#user-settings span.lang').text name
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

  create: create
