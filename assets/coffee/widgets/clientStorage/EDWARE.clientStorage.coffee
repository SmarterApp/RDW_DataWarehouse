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

###
# Edware client Storage #

This module provides client side session storage.
###
define [
  "jquery"
  "edwareUtil"
  "edwareConstants"
], ($, edwareUtil, Constants) ->

  clearAll = () ->
    ### Clears all client storage. ###
    sessionStorage.clear()
    localStorage.clear()

  loadKeyPrefix = () ->
    ### Loads user information and use user guid as key prefix. ###
    guid = ''
    $.ajax {
      # have to use a separate ajax call to avoid circular dependancy issue as it was when using dataProxy
      url: '/services/userinfo'
      type: 'POST'
      dataType: 'json'
      async: false
      success: (data) ->
        guid = edwareUtil.getGuid data.user_info
    }
    guid

  PREFIX = loadKeyPrefix()

  ### Edware client storage. ###
  class EdwareClientStorage

    constructor: (key, @isLongTerm) ->
      ### Constructor with storage key, and whether we should use localStorage vs. sessionStorage as parameter. ###
      this.key = PREFIX + key
      # By default, we use sessionStorage unless isLongTerm is true
      this.isLongTerm = if typeof @isLongTerm isnt "undefined" then @isLongTerm else false
      # Test if localStorage is supported, if not, make it sessionStorage
      if this.isLongTerm and not window.localStorage
        this.isLongTerm = false
      # No PREFIX in key for local storage since used before user_info key
      if this.isLongTerm and window.localStorage
        this.key = key
      this.storage = if this.isLongTerm then localStorage else sessionStorage
      this

    load: () ->
      ### Loads data from session storage###
      this.storage.getItem(this.key)

    save: (data) ->
      ###
      Saves data into session storage.
      Data must be able to convert to a JSON string in order to be put into session storage.
      ###
      this.storage.setItem(this.key, JSON.stringify(data))

    update: (data) ->
      ###
      Merge data into existing storage
      ###
      merged = $.extend(JSON.parse(this.load() || "{}"), data)
      this.storage.setItem(this.key, JSON.stringify(merged))

    clear: () ->
      ### Clear data ###
      this.storage.removeItem(this.key)

  ###
  Filter Storage
  ###
  filterStorage: new EdwareClientStorage('edware.filter.params')
  stickyCompStorage: new EdwareClientStorage('edware.sticky.comparison')
  EdwareClientStorage: EdwareClientStorage
  clearAll: clearAll
