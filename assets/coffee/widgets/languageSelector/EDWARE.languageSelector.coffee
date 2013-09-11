define [
  "jquery"
  "edwareDataProxy"
  "edwareUtil"
],($, edwareDataProxy, edwareUtil) ->
  
  create = (language_selector) ->
    iso_language = edwareUtil.getSelectedLanguage()
    selector = '<span class="btn-group">' +
    '<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">' +
    '<span id="selected_language" lang="' + iso_language + '">'
    options =
      async: false
      method: "GET"
    edwareDataProxy.getDatafromSource "../data/languages.json", options, (data)->
      languages = data['languages']
      selector += languages[iso_language] + '</span><span class="caret"></span>' +
      '</button>' +
      '<ul class="dropdown-menu" role="menu">'
      
      $.each languages, (lang, name) ->
        selector += '<li class="language_selections"><a href="#" id="' + lang + '" >' + name + '</a></li>'
    selector += '</ul></span>'
    language_selector.html(selector)
    $('.language_selections').on
      click: (e) ->
        e.preventDefault()
        current_selected_lang = edwareUtil.getSelectedLanguage()
        lang_id = $(this).children('a').attr "id"
        language_name = $('#' + lang_id).text()
        $('#selected_language').html language_name
        sessionStorage.setItem('language_name', language_name)
        $('#selected_language').attr('lang', lang_id)
        sessionStorage.setItem('iso_language', lang_id)
        location.reload() unless current_selected_lang is lang_id
  
  create: create