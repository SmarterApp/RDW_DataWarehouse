define [
  'jquery'
  'mustache'
  'edwareUtil'
  'edwareLoadingMask'
  'edwarePreferences'
  'edwareConstants'
], ($, Mustache, edwareUtil, edwareLoadingMask, edwarePreferences, Constants) ->

  language = edwarePreferences.getSelectedLanguage()

  URLs =
    labels: "../data/common/#{language}/labels.json"
    filters: "../data/filter/#{language}/filter.json"
    content: "../data/content/#{language}/content.json"
    common: "../data/common/#{language}/common.json"
    landingPage: "../data/content/#{language}/landingPage.json"
    stateMap: "../data/stateMap.json"

  # setup URLs for report's specific JSON
  for reportName, fileName of Constants.REPORT_JSON_NAME
    URLs[fileName] = "../data/common/#{language}/#{fileName}.json"

  DEFAULT_SETTING =
    type: 'GET'
    data: ''
    async: true
    dataType: 'json'
    contentType: 'application/json'

  onError = (xhr, ajaxOptions, thrownError, redirectOnError) ->
    # Read the redirect url on 401 Unauthorized Error
    responseHeader = xhr.getResponseHeader('Content-Type')
    # redirect to login page
    if xhr.status == 401 and /application\/json/.test(responseHeader)
      location.href = JSON.parse(xhr.responseText).redirect
    location.href = "/assets/public/error.html" if redirectOnError
    alert 1

  getDatafromSource = (sourceURL, options) ->
    if not sourceURL || not $.type(sourceURL) in ['string', 'array']
      return new TypeError('sourceURL invalid')

    options = options || {}

    # define if redirect to error page in case error occurs on server side
    if options.hasOwnProperty('redirectOnError')
      redirectOnError = options.redirectOnError
    else
      redirectOnError = true

    config = $.extend {}, DEFAULT_SETTING
    # setup settings
    config.data = JSON.stringify options.params if options.params
    config.type = options.method if options.method

    dataLoader = edwareLoadingMask.create(context: '<div></div>')
    dataLoader.show()

    sourceURL = [ sourceURL ] if $.type(sourceURL) is 'string'
    deferreds = for url in sourceURL
      $.ajax url, config

    defer = $.Deferred()
    $.when.apply($, deferreds)
      .always ->
        $('.loader').remove()
      .done ->
        if $.type(arguments[1]) is 'string'
          # single ajax call response
          data = arguments[0]
        else
          data = {} # multiple ajax calls' response
          for args in arguments
            $.extend true, data, args[0]
        defer.resolve data
      .fail (xhr, ajaxOptions, thrownError) ->
        defer.reject arguments
        onError xhr, ajaxOptions, thrownError, redirectOnError
    defer.promise()


  getDataForReport = (reportName) ->
    reportUrl = [URLs[reportName]]
    reportUrl = [] if not reportUrl
    resources = [URLs.content, URLs.common, URLs.labels].concat(reportUrl)
    defer = $.Deferred()
    getDatafromSource(resources).done (data)->
      # preprocess legend data
      for key of data['legendInfo']
        data['legendInfo'][key] = data['legendInfo'][key] if data['legendInfo'].hasOwnProperty(key)
      data['legendInfo'] = JSON.parse(Mustache.render(JSON.stringify(data['legendInfo']), {'labels':data.labels}))
      defer.resolve data
    defer.promise()

  getDataForFilter = ->
    getDatafromSource [URLs.labels, URLs.filters]

  getDataForLandingPage = ->
    getDatafromSource [URLs.labels, URLs.landingPage]


  getDatafromSource: getDatafromSource
  getDataForReport: getDataForReport
  getDataForFilter: getDataForFilter
  getDataForLandingPage: getDataForLandingPage
