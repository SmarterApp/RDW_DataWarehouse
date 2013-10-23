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


  class EdwareDownload

    constructor: () ->
      # Use any available BlobBuilder/URL implementation:
      this.BlobBuilder = window.BlobBuilder || window.WebKitBlobBuilder || window.MozBlobBuilder || window.MSBlobBuilder || window.Blob
      this.URL = window.URL || window.webkitURL || window.mozURL || window.msURL
      # IE 10 has a handy navigator.msSaveBlob method.
      navigator.saveBlob = navigator.saveBlob || navigator.msSaveBlob || navigator.mozSaveBlob || navigator.webkitSaveBlob
      window.saveAs = window.saveAs || window.webkitSaveAs || window.mozSaveAs || window.msSaveAs;

    saveAsBlob: (data, name, mimeType) ->
      blob = this.makeBlob data, mimeType
      if (window.saveAs)
        window.saveAs(blob, name)
      else
        navigator.saveBlob(blob, name)

    saveAsURI: (data, filename, mimetype) ->
      url = 'data:application/csv;charset=UTF-8,' + encodeURIComponent(data)
      link = $('<a>').html(filename).attr('href', url).attr('download', filename)[0]
      if link.download
        event = document.createEvent('MouseEvents')
        event.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0, false, false, false, false, 0, null)
        link.dispatchEvent(event)
      else
        window.open(url, '_blank', '')

    saveAsWindow: (data, filename, mimetype) ->
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