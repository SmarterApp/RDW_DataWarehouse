define ["jquery", "edwareSearch", "edwareConstants"], ($, edwareSearch, CONSTANTS) ->

  EdwareSearch = edwareSearch.EdwareSearch

  labels = {
    "prev": "Prev"
    "next": "Next"
    "SearchResultText": {
        "hasMatch": "<b id='cursor'>{{cursor}}</b> of <b>{{total}}</b> matching \"<b>{{keyword}}</b>\"",
        "notFound": "No match \"<b>{{keyword}}</b>\" in this district. Please check spelling and try again."
    }
  }

  module "EDWARE.search.create",
    setup: ->
      $("body").append "<div id='searchContainer'></div>"
      $("body").append "<div id='searchResult'></div>"
      $("body").append "<div id='gridTable'></div>"
      # mock sorted data
      $.fn.edwareSortedDataBackup = $.fn.edwareSortedData
      $.fn.edwareSortedData = ()->
        [
          {'name': 'test1'},
          {'name': 'test2'},
          {'name': 'test3'}
          {'some gabage': 'never mind'}
        ]


    teardown: ->
      $("#searchContainer").remove()
      $("#searchResult").remove()
      $("#gridTable").remove()
      $.fn.edwareSortedData = $.fn.edwareSortedDataBackup

  test "Test edwareSearchBox method", ->
    edwareSearchBox = $.fn.edwareSearchBox
    ok edwareSearchBox isnt `undefined`, "edwareBreadcrumbs.edwareSearchBox method should be defined"
    ok typeof edwareSearchBox is "function", "edwareBreadcrumbs.edwareSearchBox method should be function"

  test "Test EdwareSearch constructor", ->
    $container = $('#searchContainer')
    search = new EdwareSearch($container, labels)
    ok $container.html(), "should populate template to container"
    ok search.searchBox, "search widget should include a search box"
    ok search.searchBtn, "search widget should include a search button"

  test "Test jQuery plugin function", ->
    search = $('#searchContainer').edwareSearchBox(labels)
    ok search.searchBox, "search widget should include a search box"
    ok search.searchBtn, "search widget should include a search button"

  test "Test search function", ->
    $container = $('#searchContainer')
    search = new EdwareSearch($container, labels)
    search.searchBtn.trigger 'click'
    ok not $('.searchResult').html(), "Should display nothing if search keyword"

    search.searchBox.attr('value', 'test')
    search.searchBtn.trigger 'click'
    equal $('#cursor').text(), "1", "Should display matched information"

    search.searchBox.attr('value', 'no_match')
    search.searchBtn.trigger 'click'
    ok $('.searchResult').html().indexOf("No match") > -1, "Should display no matched information"

    search.searchBox.attr('value', 'test')
    e = $.Event("keyup", {keyCode: 13})
    #trigger pressing enter key event
    search.searchBox.trigger e
    equal $('#cursor').text(), "1", "Should display matched information"


  test "Test next and prev buttons", ->
    $container = $('#searchContainer')
    search = new EdwareSearch($container, labels)
    search.searchBox.attr('value', 'test')
    search.searchBtn.trigger 'click'
    equal $('#cursor').text(), "1", "Should display matched information"
    $('#nextBtn').click()
    equal $('#cursor').text(), "2", "Should move to next match"
    $('#prevBtn').click()
    equal $('#cursor').text(), "1", "Should move to prev match"

  test "Test ctrl-F hijack", ->
    $container = $('#searchContainer')
    search = new EdwareSearch($container, labels)
    e = $.Event("keydown", {keyCode: 70})
    e.metaKey = true
    e.ctrlKey = true
    $(window).trigger(e)
    ok $('input:focus'), "Ctrl - F should put focus on search box"

  test "Test reset", ->
    $container = $('#searchContainer')
    search = new EdwareSearch($container, labels)
    search.searchBox.attr('value', 'test')
    search.searchBtn.trigger 'click'
    $('.closeBtn').click()
    ok not search.searchBox.attr('value'), "close button should reset input box"

  test "Test reset after sorting", ->
    $container = $('#searchContainer')
    search = new EdwareSearch($container, labels)
    search.searchBox.attr('value', 'test')
    search.searchBtn.trigger 'click'
    $(document).trigger CONSTANTS.EVENTS.SORT_COLUMNS
    ok not search.searchBox.attr('value'), "close button should reset input box"
