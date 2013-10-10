###
# Edware Session Storage #

This module provides client side session storage.
###
define [
  "jquery"
  "edwareUtil"
], ($, edwareUtil) ->

  clearAll = () ->
    ### Clears all session storage. ###
    sessionStorage.clear()

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

  ### Edware session storage. ###
  class EdwareSessionStorage

    constructor: (key) ->
      ### Constructor with storage key as parameter. ###
      this.key = PREFIX + key

    load: () ->
      ### Loads data from session storage###
      sessionStorage.getItem(this.key)

    save: (data) ->
      ###
      Saves data into session storage.
      Data must be able to convert to a JSON string in order to be put into session storage.
      ###
      sessionStorage.setItem(this.key, JSON.stringify(data))
    
    update: (data) ->
      ###
      Merge data into existing storage
      ###
      merged = $.extend(JSON.parse(this.load() || "{}"), data)
      sessionStorage.setItem(this.key, JSON.stringify(merged))
    
    clear: () ->
      ### Clear data ###
      sessionStorage.removeItem(this.key)

  ###
  Filter Storage
  ###
  filterStorage: new EdwareSessionStorage('edware.filter.params')
  preferences: new EdwareSessionStorage('edware.preferences')
  stickyCompStorage: new EdwareSessionStorage('edware.sticky.comparison')
  clearAll: clearAll
