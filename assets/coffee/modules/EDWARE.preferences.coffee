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
    lang_id = iso_language.languageId if iso_language
    lang_id || edwareUtil.getUrlParams()['lang'] ||'en'

  saveSelectedLanguage = (lang) ->
    savePreferences {"languageId": lang}

  getInterimInfo = () ->
    pref = getPreferences()
    info = pref.interimDisclaimer if pref
    info || false
  
  saveInterimInfo = () ->
    savePreferences {"interimDisclaimerLoaded": true}
    
  savePreferences = (data) ->
    clientStorage.preferences.update(data)
    
  getPreferences = () ->
    JSON.parse(clientStorage.preferences.load() || "{}")
    
  saveAsmtPreference:saveAsmtPreference
  getAsmtPreference:getAsmtPreference
  getSelectedLanguage: getSelectedLanguage
  saveSelectedLanguage: saveSelectedLanguage
  getInterimInfo:getInterimInfo
  saveInterimInfo:saveInterimInfo
  savePreferences:savePreferences
  getPreferences:getPreferences