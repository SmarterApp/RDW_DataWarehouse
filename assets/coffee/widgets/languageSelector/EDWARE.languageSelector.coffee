define [
  "jquery"
  "edwareDataProxy"
  "edwarePreferences"
],($, edwareDataProxy, edwarePreferences) ->
  
  create = (language_selector, labels) ->
    language_selector.prepend $('<div class="language_selections_header"><div class="padTopBottom9"><i class="icon-globe"></i>'+labels.language+'</div><li class="divider"></li></div><div class="language_selections_body padTopBottom9"></div>')
    language_selector_body = language_selector.find('.language_selections_body')
    iso_language = edwarePreferences.getSelectedLanguage()
    options =
      async: false
      method: "GET"
    edwareDataProxy.getDatafromSource "../data/languages.json", options, (data)->
      languages = data['languages']
      
      
      $.each languages, (lang, name) ->
        language_selections = $('<li></li>')
        input = $('<input type="radio" name="language" value="' + lang + '" >' + name + '</input>')
        input.attr('checked', true) if lang is iso_language
        language_selections.append input 
        language_selector_body.append language_selections
    
    $('input[name="language"]:radio').on
      change: (e) ->
        e.preventDefault()
        current_selected_lang = edwarePreferences.getSelectedLanguage()
        lang_id = $(this).attr "value"
        language_name = $('#' + lang_id).text()
        edwarePreferences.saveSelectedLanguage lang_id
        location.reload() unless current_selected_lang is lang_id
  
  create: create