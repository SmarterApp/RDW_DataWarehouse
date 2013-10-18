define [
  "jquery"
  "mustache"
  "edwareConstants"
], ($, Mustache, Constants) ->

  class CSVBuilder
  
    constructor: (@reportType) ->

    build: (@data) ->

    getFileName: () ->
      this.reportType + '_' + new Date().getTime()

    CSVBuilder::getPropertyByString = (object, fields)->
      # fields = fields.replace(/\[(\w+)\]/g, '.$1'); # convert indexefields to propertiefields
      # fields = fields.replace(/^\./, '');           # fieldstrip a leading dot
      properties = fields.split('.')
      while properties.length
        property = properties.shift()
        if object[property]
          object = object[property]
        else
          return
      return object


  class ISRBuilder extends CSVBuilder
  
    build: (data) ->
      'hello world'
      

  class LOSBuilder extends CSVBuilder
  
    build: (data) ->
      return 'this,is,los'
      records = data.map (record)->
        result = []
        result.push record.name
        result.push record.results.subject1.asmt_subject
        result.push record.results.subject1.total
        result.push record.results.subject2.asmt_subject
        result.push record.results.subject2.total
        result.join Constants.DELIMITOR.COMMA
      records.join Constants.DELIMITOR.NEWLINE      


  class CPopBuilder extends CSVBuilder
  
    build: (data, config) ->
      columns = this.toExportColumns config
      records = data.map (record)->
        result = []
        for column in columns
          result.push CSVBuilder::getPropertyByString(record, column.field) if column.export
        result.join Constants.DELIMITOR.COMMA
      records.join Constants.DELIMITOR.NEWLINE

    toExportColumns: (config)->
      columns = []
      for column in config
        $.map column.items, (item)->
          columns.push item
      columns
      
  builderFactory = (reportType)->
    switch reportType
      when Constants.REPORT_TYPE.CPOP then new CPopBuilder(reportType)
      when Constants.REPORT_TYPE.LOS then new LOSBuilder(reportType)
      when Constants.REPORT_TYPE.ISR then new ISRBuilder(reportType)

  download = (content, filename) ->
    uri = 'data:application/csv;charset=UTF-8,' + encodeURIComponent(content)
    link = $('<a>').html(filename).attr('href', uri).attr('download', filename)[0]
    if link.download and filename
      # have to append link to body element, or it's not gonna work in Firefox
      $('body').append link
      # download with file name
      link.click()
      $(link).remove()
    else
      # download as anonymous file
      window.open(uri, '_parent')

  exportCSV = (reportType, model) ->
    builder = builderFactory(reportType)
    download builder.build(model.data, model.config), builder.getFileName()


  exportCSV: exportCSV
