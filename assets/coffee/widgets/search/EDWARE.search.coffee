define [
  "jquery"
], ($) ->

  class EdwareSearch

    constructor: (@labels, @callback) ->
      @initialize()

    initialize: () ->
      template = "<input id='searchInput' class='pull-right form-control' tabindex='2' type='text' role='search' placeholder='" + this.labels.search + "'>"
      $('#search').html template
      this.bindEvents()

    bindEvents: () ->
      self = this
      $('#searchInput').keyup (e) -> 
        if e.keyCode is 13
          self.query = this.value
          self.callback()

      $(window).keydown (e) ->
        # Listens for ctrl-f
        if (e.ctrlKey or e.metaKey) and e.keyCode is 70
          e.preventDefault()
          $('#searchInput').focus()

    getSearchResults : (info, field) ->
      results = $.extend(true, {}, info);
      # If a search query criteria is specified, filter it out
      if this.query
        query = this.query.toLowerCase()
        returnData = []
        if results.data
          for data in results.data
            name = data[field].toLowerCase()
            if name.indexOf(query) > -1
              returnData.push data
          results.data = returnData
      results

  EdwareSearch: EdwareSearch
