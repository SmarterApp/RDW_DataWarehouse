define [
  "jquery"
  "mustache"
  "edwareConstants"
], ($, Mustache, Constants) ->

  class CSVBuilder
  
    constructor: (@table, @reportType) ->

    build: () ->
      records = ('' for i in [1..10]) # fixed first 10 rows
      # build header
      records = records.concat this.buildHeader()
      # build body
      records = records.concat this.buildContent()
      records.join Constants.DELIMITOR.NEWLINE 

    buildHeader: () ->
      result = []
      footer = this.table.footerData()
      for key, value of footer
        exportField = $(value).find('div.export')
        result.push exportField.find('span:eq(1)').html() if exportField[0]
      result.join Constants.DELIMITOR.COMMA

    buildContent: () ->
      # summary
      data = []
      data = data.concat this.table.footerData()
      # table body
      data = data.concat this.table.getRowData()
      $.map data, (record)->
        result = []
        for key, value of record
          exportField = $(value).find('div.export')
          result.push exportField.find('span:eq(0)').html() if exportField[0]
        result.join Constants.DELIMITOR.COMMA

    getFileName: () ->
      this.reportType + '_' + new Date().getTime() + '.csv'

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

  
  $.fn.edwareExport = (reportType)->
    builder = new CSVBuilder(this, reportType)
    download builder.build(), builder.getFileName()