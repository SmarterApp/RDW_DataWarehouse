define [
  "jquery"
  "mustache"
  "edwareConstants"
], ($, Mustache, Constants) ->



  class CSVBuilder
  
    constructor: () ->

    build: (@data) ->

    getFileName: () ->
      'hello'

  class CPopBuilder extends CSVBuilder
  
    build: (@data) ->
      records = this.data.map (record)->
        result = []
        result.push record.name
        result.push record.results.subject1.asmt_subject
        result.push record.results.subject1.total
        result.push record.results.subject2.asmt_subject
        result.push record.results.subject2.total
        result.join Constants.DELIMITOR.COMMA
      records.join Constants.DELIMITOR.NEWLINE
      
  builderFactory = (reportType)->
    switch reportType
      when Constants.REPORT_TYPE.CPOP then new CPopBuilder()
      when Constants.REPORT_TYPE.LOS then new LOSBuilder()
      when Constants.REPORT_TYPE.ISR then new ISRBuilder()

  download = (content, filename) ->
    uri = 'data:application/csv;charset=UTF-8,' + encodeURIComponent(content)
    link = $('a').html(filename)
    if (typeof link.download != "undefined") and filename
      # download with file name
      link.setAttribute("href", uri)
      link.setAttribute("download", filename)
      link.click();
    else
      # download as anonymous file
      window.open(uri);

  exportCSV = (reportType, data) ->
    builder = builderFactory(reportType)
    download builder.build(data), builder.getFileName()


  exportCSV: exportCSV
