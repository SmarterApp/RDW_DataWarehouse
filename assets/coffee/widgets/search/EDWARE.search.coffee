define [
  "jquery"
  "mustache"
  "text!SearchBoxTemplate"
  "text!SearchResultTemplate"
], ($, Mustache, SearchBoxTemplate, SearchResultTemplate) ->

  class EdwareSearch

    constructor: (@container, @labels) ->
      @initialize()
      @bindEvents()

    initialize: () ->
      @container.html Mustache.to_html SearchBoxTemplate,
        labels: @labels
      @searchBox = $('.searchbox', @container)
      @searchBtn = $('.searchBtn', @container)
      @searchResult = $('#searchResult')

    bindEvents: () ->
      self = this
      # press enter key event
      @searchBox.keyup (e) ->
        if e.keyCode is 13
          self.search @value.trim()

      @searchBtn.on 'click', () ->
        keyword = self.searchBox.attr('value')
        self.search keyword

      @searchResult.on 'click', '.closeBtn', ()->
        $('.searchResult').remove()
        self.searchBox.attr('value', '')

      # hijack browser's `Ctrl + F` functionality
      $(window).keydown (e) ->
        # Listens for ctrl-f
        if (e.ctrlKey or e.metaKey) and e.keyCode is 70
          e.preventDefault()
          self.searchBox.focus()

      @searchResult.on 'click', '#prevBtn', ()->
        self.results.previous()
      @searchResult.on 'click', '#nextBtn', ()->
        self.results.next()

    search: (keyword) ->
      # do nothing if no search keyword
      keyword = keyword.trim()
      return if not keyword
      @results = new ResultIterator keyword, @update.bind(this)
      @displayResults(keyword)

    displayResults: (keyword)->
      total = @results.size()
      hasMatch = total isnt 0
      @searchResult.html Mustache.to_html SearchResultTemplate,
        hasMatch: hasMatch
        total: total
        keyword: keyword
        labels: @labels
      # move to first record only when a match found
      @update @results.offset(), @results.index() if hasMatch

    update: (offset, cursor) ->
      $("#cursor", @searchResult).text cursor
      rowHeight = @getRowHeight()
      $('.ui-jqgrid-bdiv').scrollTop(offset * rowHeight)
      # TODO: to render match in a different color


    getRowHeight: () ->
      return @rowHeight if @rowHeight
      @rowHeight = $('.jqgrow').height()
      return @rowHeight

  class ResultIterator

    constructor: (keyword, @callback) ->
      # get grid data in sorted order
      keyword = keyword.toLowerCase()
      rows = $('#gridTable').edwareSortedData()
      @data = []
      for row, index in rows
        if @contains(row, keyword)
          @data.push index
      @cursor = 0

    contains: (row, keyword) ->
      value = row['name'] || row['student_full_name']
      if not value
        return false
      value.toLowerCase().indexOf(keyword) > -1

    index: () ->
      @cursor + 1

    offset: () ->
      @data[@cursor]

    size: () ->
      @data.length

    next: () ->
      @cursor = (@cursor + 1) % @data.length
      @callback @offset(), @index()

    previous: () ->
      @cursor = (@cursor - 1 + @data.length) % @data.length
      @callback @offset(), @index()


  $.fn.edwareSearchBox = (labels) ->
    new EdwareSearch(@, labels)

  EdwareSearch: EdwareSearch
