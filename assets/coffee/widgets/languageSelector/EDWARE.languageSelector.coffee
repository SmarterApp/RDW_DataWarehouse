define [
  "jquery"
  "edwareDataProxy"
  "edwarePreferences"
],($, edwareDataProxy, edwarePreferences) ->

  create = (language_selector, labels) ->
    language_selector.prepend $('<div class="language_selections_header"><div class="padTopBottom9"><i class="icon-globe"></i>'+labels.language+'</div><li class="divider" role="radio"></li></div><div class="language_selections_body padTopBottom9"></div>')
    language_selector_body = language_selector.find('.language_selections_body')
    iso_language = edwarePreferences.getSelectedLanguage()
    loadingLanguage = edwareDataProxy.getDatafromSource "../data/languages.json"
    loadingLanguage.done (data)->
      languages = data['languages']

      $.each languages, (lang, name) ->
        language_selections = $('<li></li>')
        input = $("<label><input type='radio' name='language' value='#{lang}'>#{name}</input></label>")
        if lang is iso_language
          input.find('input').attr('checked', true)
          $('#user-settings span.lang').text name
        language_selections.append input
        language_selector_body.append language_selections

      $(document).on 'change', 'input[name="language"]:radio', (e)->
        e.preventDefault()
        current_selected_lang = edwarePreferences.getSelectedLanguage()
        lang_id = $(this).attr "value"
        language_name = $('#' + lang_id).text()
        edwarePreferences.saveSelectedLanguage lang_id
        location.reload() unless current_selected_lang is lang_id

  create: create
