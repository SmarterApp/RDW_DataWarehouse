define [
  'edwareSessionStorage'
], (clientStorage) ->
  
  getSelectedLanguage = () ->
    iso_language = clientStorage.i18nStorage.load()
    lang_id = JSON.parse(iso_language).language_id if iso_language
    lang_id || 'en'

  saveSelectedLanguage = (item) ->
    clientStorage.i18nStorage.save(item)

  getSelectedLanguage: getSelectedLanguage
  saveSelectedLanguage: saveSelectedLanguage