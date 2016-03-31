###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

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
    asmtYear = pref[pref["stateCode"] + "asmtYear"]
    asmtYear || parseInt(edwareUtil.getUrlParams()["asmtYear"])

  getDateTaken = () ->
    pref = getPreferences() || {}
    pref["ISRAsmt"]?.date_taken

  getAsmtType = () ->
    pref = getPreferences() || {}
    pref["asmt"]?.asmt_type

  saveAsmtPreference = (asmt) ->
    savePreferences {"asmt" : asmt}

  getAsmtPreference = () ->
    pref = getPreferences() || {}
    pref['asmt']  || {}

  saveAsmtForISR = (asmt) ->
    savePreferences {"ISRAsmt": asmt}

  getAsmtForISR = () ->
    pref = getPreferences() || {}
    pref['ISRAsmt']

  getAsmtTypeForISR = () ->
    pref = getAsmtForISR() || {}
    pref?.asmt_type

  getAsmtYearForISR = () ->
    pref = getAsmtForISR() || {}
    pref?.asmt_period_year

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

  isExpandedColumn = (columnName) ->
    getExpandedColumns()[columnName]

  getExpandedColumns = () ->
    pref = getPreferences()
    pref = {} if not pref
    pref["expandedColumns"] || {}

  saveExpandedColumns = (column) ->
    pref = getExpandedColumns()
    pref[column] = true
    savePreferences {"expandedColumns": pref}

  removeExpandedColumns = (column) ->
    pref = getExpandedColumns()
    delete pref[column]
    savePreferences {"expandedColumns": pref}

  getQuickLinksState = () ->
    pref = getPreferences() || {}
    pref["quickLinks"]

  saveQuickLinksState = (state) ->
    savePreferences { "quickLinks" : state }, false

  getQuickLinksSchoolBound = () ->
    pref = getPreferences() || {}
    pref["quickLinksSchoolBound"]

  saveQuickLinksSchoolBound = (quickLinksSchoolBound) ->
    savePreferences {"quickLinksSchoolBound": quickLinksSchoolBound}

  getQuickLinksDistrictBound = () ->
    pref = getPreferences() || {}
    pref["quickLinksDistrictBound"]

  saveQuickLinksDistrictBound = (quickLinksDistrictBound) ->
    savePreferences {"quickLinksDistrictBound": quickLinksDistrictBound}

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
  getDateTaken: getDateTaken
  getAsmtType: getAsmtType
  saveAsmtForISR: saveAsmtForISR
  getAsmtForISR: getAsmtForISR
  getAsmtTypeForISR: getAsmtTypeForISR
  getAsmtYearForISR: getAsmtYearForISR
  getFilters: getFilters
  saveAsmtView: saveAsmtView
  getAsmtView: getAsmtView
  getExpandedColumns: getExpandedColumns
  saveExpandedColumns: saveExpandedColumns
  removeExpandedColumns: removeExpandedColumns
  isExpandedColumn: isExpandedColumn
  saveQuickLinksState: saveQuickLinksState
  getQuickLinksState: getQuickLinksState
  saveQuickLinksSchoolBound:saveQuickLinksSchoolBound
  getQuickLinksSchoolBound:getQuickLinksSchoolBound
  saveQuickLinksDistrictBound:saveQuickLinksDistrictBound
  getQuickLinksDistrictBound:getQuickLinksDistrictBound
