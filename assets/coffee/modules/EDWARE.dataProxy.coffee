define [
  "jquery"
  "mustache"
  "edwareUtil"
  "edwareLoadingMask"
  'edwarePreferences'
  'edwareConstants'
], ($, Mustache, edwareUtil, edwareLoadingMask, edwarePreferences, Constants) ->

  language = edwarePreferences.getSelectedLanguage()

  URLs =
    labels: '../data/common/' + language + '/labels.json',
    filters: '../data/filter/' + language + '/filter.json',
    content: '../data/content/' + language + '/content.json',
    common: '../data/common/' + language + '/common.json'

  URLs[Constants.REPORT_JSON_NAME.CPOP] = '../data/common/' + language + '/' + Constants.REPORT_JSON_NAME.CPOP + '.json'
  URLs[Constants.REPORT_JSON_NAME.LOS] = '../data/common/' + language + '/' + Constants.REPORT_JSON_NAME.LOS + '.json'
  URLs[Constants.REPORT_JSON_NAME.ISR] = '../data/common/' + language + '/' + Constants.REPORT_JSON_NAME.ISR + '.json'

  DEFAULT_SETTING =
    type: 'GET'
    data: ''
    async: true
    dataType: "json"
    contentType: "application/json"
    onSuccess: (data)->
      # simply return data by default
      data
    onError: (xhr, ajaxOptions, thrownError) ->
      redirect_url = "/assets/public/error.html"
      # Read the redirect url on 401 Unauthorized Error
      if xhr.status == 401 and xhr.getResponseHeader('Content-Type').indexOf("application/json") != -1
        response = JSON.parse(xhr.responseText)
        redirect_url = response.redirect
      # Redirect the user to the appropriate url
      #location.href = redirect_url

  #
  #    * Get data from the server via ajax call
  #    * @param sourceURL - The API call
  #    * @param options :optional -  contains configs like method, async, data for "POST" etc.
  #    * @param callback :optional- callback function
  #
  getDatafromSource = (sourceURL) ->
    return new TypeError("sourceURL invalid") unless $.type(sourceURL) in ["string", "array"]
    options = if $.type(arguments[1]) is 'object' then arguments[1] else {}
    callback = arguments[1] if $.type(arguments[1]) is 'function'
    callback = arguments[2] if $.type(arguments[2]) is 'function'

    config = $.extend {}, DEFAULT_SETTING
    # setup settings
    config.data = JSON.stringify options.params if options.params
    config.type = options.method if options.method
    config.onSuccess = callback if callback

    dataLoader = edwareLoadingMask.create(context: "<div></div>")
    dataLoader.show()

    sourceURL = [ sourceURL ] if $.type(sourceURL) is "string"
    deferreds = for url in sourceURL
      $.ajax url, config

    # send ajax call
    $.when.apply($, deferreds)
      .always ->
        $('.loader').remove()
      .done ()->
        if $.type(arguments[1]) is "string" # single ajax call response
          data = arguments[0]
        else
          data = {} # multiple ajax calls' response
          for args in arguments
            $.extend true, data, args[0]
        config.onSuccess data
      .fail (xhr, ajaxOptions, thrownError) ->
        console.error thrownError
        config.onError xhr, ajaxOptions, thrownError


  getDataForReport = (reportName) ->
    reportUrl = URLs[reportName]
    json_url = [ URLs.content, URLs.common, URLs.labels, reportUrl]
    defer = $.Deferred()
    getDatafromSource json_url, (data)->
      for key of data['legendInfo']
        data['legendInfo'][key] = data['legendInfo'][key] if data['legendInfo'].hasOwnProperty(key)
      data['legendInfo'] = JSON.parse(Mustache.render(JSON.stringify(data['legendInfo']), {"labels":data.labels}))
      defer.resolve data
    defer.promise()

  getDataForFilter = ->
    defer = $.Deferred()
    getDatafromSource [URLs.labels, URLs.filters], (data)->
      defer.resolve data
    defer.promise()


  getDatafromSource: getDatafromSource
  getDataForReport: getDataForReport
  getDataForFilter: getDataForFilter
