define [
  "jquery"
  "edwareDataProxy"
  "edwarePreferences"
],($, edwareDataProxy, edwarePreferences) ->
  
  create = (language_selector, labels) ->
    language_selector.append $('<i class="icon-globe"></i>'+labels.language+'<li class="divider"></li>')
    iso_language = edwarePreferences.getSelectedLanguage()
    selector = ''
    options =
      async: false
      method: "GET"
    edwareDataProxy.getDatafromSource "../data/languages.json", options, (data)->
      languages = data['languages']
      
      
      $.each languages, (lang, name) ->
        language_selections = $('<li class="language_selections"></li>')
        input = $('<input type="radio" name="language" value="' + lang + '" >' + name + '</input>')
        input.attr('checked', true) if lang is iso_language
        language_selections.append(input)
        language_selector.append language_selections
    
    language_selector.append($(selector))
    $('input[name="language"]:radio').on
      change: (e) ->
        e.preventDefault()
        current_selected_lang = edwarePreferences.getSelectedLanguage()
        lang_id = $(this).attr "value"
        language_name = $('#' + lang_id).text()
        edwarePreferences.saveSelectedLanguage lang_id
        location.reload() unless current_selected_lang is lang_id
  
  create: create