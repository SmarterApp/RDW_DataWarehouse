define [
  'edwareSessionStorage'
], (clientStorage) ->
  
  getSelectedLanguage = () ->
    iso_language = clientStorage.i18nStorage.load()
    lang_id = JSON.parse(iso_language).language_id if iso_language
    lang_id || 'en'

  saveSelectedLanguage = (item) ->
    clientStorage.i18nStorage.save(item)

  saveResources = (data) ->
    this.i18n_data = data

  getMessage = (key) ->
    this.i18n_data[key]

  getSelectedLanguage: getSelectedLanguage
  saveSelectedLanguage: saveSelectedLanguage
  saveResources: saveResources
  getMessage: getMessage