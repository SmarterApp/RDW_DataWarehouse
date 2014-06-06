define [
  "jquery"
  "mustache"
  "text!SearchBoxTemplate"
  "text!SearchResultTemplate"
  "edwareConstants"
  "edwareGrid"
], ($, Mustache, SearchBoxTemplate, SearchResultTemplate, CONSTANTS, edwareGrid) ->

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
        self.reset()

      $(document).on CONSTANTS.EVENTS.SORT_COLUMNS, ()->
        self.reset()

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

    reset: ()->
      $('.searchResult').remove()
      @searchBox.attr('value', '')
      @removeHighlight()
      @keyword = null
      # TODO: may need better mechanism to adjust height
      edwareGrid.adjustHeight()

    search: (keyword) ->
      # do nothing if no search keyword
      @keyword = keyword.trim()
      return if not @keyword
      @results = new ResultIterator @keyword, @update.bind(this)
      @displayResults()

    displayResults: ()->
      message = @getMessage()
      hasMatch = @results.size() isnt 0
      @searchResult.html Mustache.to_html SearchResultTemplate,
        hasMatch: hasMatch
        labels: @labels
        message: message
      # move to first record only when a match found
      @update @results.offset(), @results.index() if hasMatch
      # adjust height to accommodate last row
      edwareGrid.adjustHeight()

    getMessage: ()->
      total = @results.size()
      hasMatch = total isnt 0
      if hasMatch
        MessageTemplate = @labels.SearchResultText.hasMatch
      else
        MessageTemplate = @labels.SearchResultText.notFound
      message = Mustache.to_html MessageTemplate,
        total: total
        keyword: @keyword
      message

    update: (offset, cursor) ->
      $("#cursor", @searchResult).text cursor
      rowHeight = @getRowHeight()
      $('.ui-jqgrid-bdiv').scrollTop(offset * rowHeight)
      # Highlight active match
      @offset = offset
      @addHighlight()

    addHighlight: () ->
      @removeHighlight()
      # ensures that we're only highlighting when there's a search word
      return if not @keyword
      @lastHighlightedElement = $('#link_' + $('#gridTable').jqGrid('getGridParam', 'data')[@offset]['rowId'])
      text = @lastHighlightedElement.data('value')
      if text
        idx = text.toLowerCase().indexOf(@keyword.toLowerCase())
        @lastHighlightedElement.html(text.substr(0, idx) + "<span class='searchHighlight'>" + text.substr(idx, @keyword.length) + "</span>" + text.substr(idx + @keyword.length))

    removeHighlight: () ->
      if @lastHighlightedElement
        @lastHighlightedElement.html(@lastHighlightedElement.data('value'))
        @lastHighlightedElement = null

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
