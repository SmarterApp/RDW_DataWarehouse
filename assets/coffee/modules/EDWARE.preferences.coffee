define [
  "jquery"
  "edwareClientStorage"
  "edwareUtil"
  "edwareConstants"
], ($, clientStorage, edwareUtil, Constants) ->

  KEY = 'edware.preferences'

  shortTermStorage = new clientStorage.EdwareClientStorage KEY, false
  longTermStorage = new clientStorage.EdwareClientStorage KEY, true

  # On logout, clear storage
  $(document).on 'click', '#logout_button', () ->
    shortTermStorage.clear()

  saveStateCode = (code) ->
    savePreferences {"stateCode": code}

  getStateCode = () ->
    pref = getPreferences() || {}
    pref["stateCode"]

  saveAsmtYearPreference = (year) ->
    sc = getStateCode()
    set = {}
    set[sc + "asmtYear"] = year
    savePreferences set

  getAsmtYearPreference = () ->
    pref = getPreferences() || {}
    pref[pref["stateCode"] + "asmtYear"]

  getEffectiveDate = () ->
    pref = getPreferences() || {}
    pref["ISRAsmt"]?.effectiveDate

  getAsmtType = () ->
    pref = getPreferences() || {}
    pref["ISRAsmt"]?.asmtType

  saveAsmtPreference = (asmt) ->
    savePreferences {"asmt" : asmt}

  getAsmtPreference = () ->
    pref = getPreferences() || {}
    pref['asmt']

  saveAsmtForISR = (asmt) ->
    savePreferences {"ISRAsmt": asmt}

  getAsmtForISR = () ->
    pref = getPreferences() || {}
    pref['ISRAsmt']

  getAsmtView = () ->
    pref = getPreferences() || {}
    pref['asmtView']

  saveAsmtView = (asmtView) ->
    savePreferences {"asmtView": asmtView}

  clearAsmtPreference = ->
    saveAsmtPreference {}

  saveSubjectPreference = (asmtSubject) ->
    savePreferences {"asmtSubject": asmtSubject}

  getSubjectPreference = () ->
    pref = getPreferences()
    pref = {} if not pref
    pref["asmtSubject"] || []

  getSelectedLanguage = () ->
    iso_language = getPreferences true
    lang_id = iso_language.languageId if iso_language
    lang_id || edwareUtil.getUrlParams()['lang'] ||'en'

  saveSelectedLanguage = (lang) ->
    savePreferences {"languageId": lang}, true

  getInterimInfo = () ->
    pref = getPreferences true
    info = pref.interimDisclaimerLoaded if pref
    info || false

  saveInterimInfo = () ->
    savePreferences {"interimDisclaimerLoaded": true}, true

  # Returns storage based whether long term is set to true
  getStorage = (isLongTerm) ->
    isLongTerm = if typeof isLongTerm isnt "undefined" then isLongTerm else false
    if isLongTerm then longTermStorage else shortTermStorage

  savePreferences = (data, isLongTerm) ->
    getStorage(isLongTerm).update(data)

  getPreferences = (isLongTerm) ->
    JSON.parse(getStorage(isLongTerm).load() || "{}")

  getFilters = () ->
    JSON.parse(clientStorage.filterStorage.load() || "{}")

  saveStateCode:saveStateCode
  getStateCode:getStateCode
  saveAsmtPreference:saveAsmtPreference
  getAsmtPreference:getAsmtPreference
  clearAsmtPreference: clearAsmtPreference
  saveSubjectPreference:saveSubjectPreference
  getSubjectPreference:getSubjectPreference
  getSelectedLanguage: getSelectedLanguage
  saveSelectedLanguage: saveSelectedLanguage
  getInterimInfo:getInterimInfo
  saveInterimInfo:saveInterimInfo
  saveAsmtYearPreference: saveAsmtYearPreference
  getAsmtYearPreference: getAsmtYearPreference
  getEffectiveDate: getEffectiveDate
  getAsmtType: getAsmtType
  saveAsmtForISR: saveAsmtForISR
  getAsmtForISR: getAsmtForISR
  getFilters: getFilters
  saveAsmtView: saveAsmtView
  getAsmtView: getAsmtView
