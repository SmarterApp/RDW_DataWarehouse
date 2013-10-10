define [
  "jquery"
  "edwareSessionStorage"
  "edwareUtil"
], ($, clientStorage, edwareUtil) ->
  
  saveAsmtPreference = (asmtType) ->
    savePreferences {"asmtType": asmtType}
    
  getAsmtPreference = () ->
    pref = getPreferences()
    pref = {} if not pref
    pref["asmtType"] || 'Summative'
  
  getSelectedLanguage = () ->
    iso_language = getPreferences()
    lang_id = iso_language.language_id if iso_language
    lang_id || edwareUtil.getUrlParams()['lang'] ||'en'

  saveSelectedLanguage = (lang) ->
    savePreferences {"language_id": lang}

  savePreferences = (data) ->
    clientStorage.preferences.update(data)
    
  getPreferences = () ->
    JSON.parse(clientStorage.preferences.load() || "{}")
    
  saveAsmtPreference:saveAsmtPreference
  getAsmtPreference:getAsmtPreference
  getSelectedLanguage: getSelectedLanguage
  saveSelectedLanguage: saveSelectedLanguage
  savePreferences:savePreferences
  getPreferences:getPreferences