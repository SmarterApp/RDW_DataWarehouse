define [
  "jquery"
  "mustache"
  "edwareConstants"
  "edwareClientStorage"
  "edwareUtil"
], ($, Mustache, Constants, edwareClientStorage, edwareUtil) ->

  TIMESTAMP_TEMPLATE = '{{mm}}-{{dd}}-{{yyyy}} {{hh}}:{{MM}}:{{ss}}'

  class CSVBuilder
  
    constructor: (@table, @reportType) ->
      current = new Date()
      this.timestamp = Mustache.to_html TIMESTAMP_TEMPLATE, {
        yyyy: current.getFullYear()
        mm: current.getMonth()
        dd: current.getDate()
        hh: current.getHours()
        MM: current.getMinutes()
        ss: current.getSeconds()
      }
      this.title =  $('.title h2').text()
      this.sortBy = this.table.jqGrid('getGridParam','sortname');
      this.asmtType = $('#selectedAsmtType').text() || 'Summative'
      this.isSticky = $('.stickyState').data('label')
      
    build: () ->
      records = [] # fixed first 10 rows
      # build header
      records = records.concat this.buildTitle()
      # build body
      records = records.concat this.buildContent()
      records.join Constants.DELIMITOR.NEWLINE

    buildTitle: () ->
      records = []
      # build title
      records.push edwareUtil.escapeCSV ['Report Name', this.title]
      # build timestamp and username
      records.push edwareUtil.escapeCSV ['Generated Date', this.timestamp]
      # build filters
      records.push edwareUtil.escapeCSV ['Filters', this.buildFilters()]
      records.push edwareUtil.escapeCSV ['Sort By', this.sortBy]
      records.push edwareUtil.escapeCSV ['Comparison', this.isSticky]
      records.push edwareUtil.escapeCSV ['Assessment Type', this.asmtType]
      for i in [records.length .. 9] # fix first 10 rows as headers
        records.push ''
      records

    buildFilters: () ->
      params = edwareClientStorage.filterStorage.load()
      for key, value of JSON.parse(params)
        key + ":" + value

    buildContent: () ->
      result = []
      rowData = this.table.getRowData()
      # build column names
      result.push this.getColumnNames(rowData[0]) # row 0 is header
      # build summary
      footerData = this.table.footerData()
      if not $.isEmptyObject(footerData)
        result.push this.getColumnValues(footerData)
      # build table grid
      for record, index in rowData
        result.push this.getColumnValues(record)
      result

    getColumnNames: (record) ->
      this.buildRow(record, 'export-name')

    getColumnValues: (record) ->
      this.buildRow(record, 'export-value')

    buildRow: (record, field) ->
      columnValues = []
      for key, value of record
        exportField = $(value)
        continue if not exportField.hasClass('export')
        exportField.find('span.hidden').each () ->
          $this = $(this)
          columnValues.push $this.data(field)
      columnValues = edwareUtil.escapeCSV columnValues
      columnValues.join(Constants.DELIMITOR.COMMA)
      
    getFileName: () ->
      this.reportType + '_' + this.timestamp + '.csv'


  class EdwareDownload

    constructor: () ->
      # Use any available BlobBuilder/URL implementation:
      this.BlobBuilder = window.BlobBuilder || window.WebKitBlobBuilder || window.MozBlobBuilder || window.MSBlobBuilder || window.Blob
      this.URL = window.URL || window.webkitURL || window.mozURL || window.msURL
      # IE 10 has a handy navigator.msSaveBlob method.
      navigator.saveBlob = navigator.saveBlob || navigator.msSaveBlob || navigator.mozSaveBlob || navigator.webkitSaveBlob
      window.saveAs = window.saveAs || window.webkitSaveAs || window.mozSaveAs || window.msSaveAs;

    saveAsBlob: (data, name, mimeType) ->
      # Support IE10+
      blob = this.makeBlob data, mimeType
      if (window.saveAs)
        window.saveAs(blob, name)
      else
        navigator.saveBlob(blob, name)

    saveAsURI: (data, filename, mimetype) ->
      # Support Chrome, FF, Safari
      url = 'data:application/csv;charset=UTF-8,' + encodeURIComponent(data)
      link = $('<a>').html(filename).attr('href', url).attr('download', filename)[0]
      if link.download
        event = document.createEvent('MouseEvents')
        event.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0, false, false, false, false, 0, null)
        link.dispatchEvent(event)
      else
        window.open(url, '_blank', '')

    saveAsWindow: (data, filename, mimetype) ->
      # Suppport other browsers
      x = window.open();
      x.document.open(mimetype, "replace");
      x.document.write(data);
      x.document.close();

    create: () ->
      # Blobs and saveAs (or saveBlob)	:
      if (this.BlobBuilder && (window.saveAs || navigator.saveBlob))
        # Support IE 10+
        return this.saveAsBlob.bind(this)
      # data:-URLs:
      else if (!/\bMSIE\b/.test(navigator.userAgent))
        # Blobs and object URLs, support webkit and gecko
        # IE does not support URLs longer than 2048 characters (actually bytes), so it is useless for data:-URLs.
        return this.saveAsURI.bind(this)
      else
        return this.saveAsWindow.bind(this)

    makeBlob: (data, mimetype) ->
      try
        return new Blob([data],{type:mimetype||"application/octet-stream"})
      catch e
        builder = new this.BlobBuilder()
        builder.append(data)
        return builder.getBlob(mimetype||"application/octet-stream")

  download = (content, filename) ->
    save = new EdwareDownload().create()
    save content, filename, 'application/csv'

  $.fn.edwareExport = (reportType)->
    this.eagerLoad()
    builder = new CSVBuilder(this, reportType)
    download builder.build(), builder.getFileName()
    this.lazyLoad()