define [
  'edwareSessionStorage'
  'edwareUtil'
], (clientStorage, edwareUtil) ->
  
  getSelectedLanguage = () ->
    iso_language = clientStorage.preferences.load()
    lang_id = JSON.parse(iso_language).language_id if iso_language
    lang_id || edwareUtil.getUrlParams()['lang'] ||'en'

  saveSelectedLanguage = (item) ->
    clientStorage.preferences.update(item)

  getSelectedLanguage: getSelectedLanguage
  saveSelectedLanguage: saveSelectedLanguage