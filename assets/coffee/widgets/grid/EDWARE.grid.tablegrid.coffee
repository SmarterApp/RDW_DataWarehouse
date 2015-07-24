define [
  'jquery'
  'jqGrid'
  'edwareUtil'
  'edwareGridFormatters'
  'edwareConstants'
], ($, jqGrid, edwareUtil, edwareGridFormatters, CONSTANTS) ->

  COMPONENTS_SELECTORS = ['#header', '#breadcrumb', '#infoBar', '#actionBar', '#searchResult',
    '#stickyCompareSection', '.selectedFilter_panel', '.ui-jqgrid-hdiv', '.ui-jqgrid-sdiv']

  DEFAULT_CONFIG =
    tableId: 'gridTable'
    data: undefined
    options:
      gridHeight: window.innerHeight * 0.6 #default grid height
      datatype: "local"
      height: "auto"
      viewrecords: true
      autoencode: true
      frozenColumns: false
      rowNum: 100
      gridview: true
      scroll: 1
      shrinkToFit: false
      defaultWidth: 980
      loadComplete: () ->

  EXPAND_ICONS = {
    'EXPANDED': "<a href='#' class='expand-icon edware-icon-collapse-expand-minus'></a>"
    'COLLAPSED': "<a href='#' class='expand-icon edware-icon-collapse-expand-plus'></a>"
  }

  class EdwareGrid

    constructor: (@table, columns, @options, @footer) ->
      this.columns = this.setSortedColumn columns
      this.options.footerrow = true if this.footer
      self = this
      this.options.loadComplete = () ->
        self.afterLoadComplete()

    bindEvents: ()->
      # reset focus after sorting
      self = this
      $('.ui-jqgrid-sortable').find('a, span').click (e)->
        id = $(this).parent().attr('id')
        lastFocus = "##{id}"
        # escape dot in element id
        self.lastFocus = lastFocus.replace(/\./gi, '\\.')
        # emit sorting event to other listeners
        $(document).trigger CONSTANTS.EVENTS.SORT_COLUMNS
        createPrintMedia()

      $('a.expand-icon').click (e) ->
        $(document).trigger CONSTANTS.EVENTS.EXPAND_COLUMN, $(this)

      # load more data when focus on first and last row by triggering
      # scrolling event.
      bodyTable = $('.ui-jqgrid-btable')
      bodyDiv = bodyTable.closest('.ui-jqgrid-bdiv')
      bodyTable.on 'focus', 'tr:last-child ', ->
        offset = bodyDiv.scrollTop()
        bodyDiv.scrollTop(offset + 10)
      # The first row that contains user content is
      # actually the second `tr`
      bodyTable.on 'focus', 'tr:nth-child(2) ', ->
        offset = bodyDiv.scrollTop()
        bodyDiv.scrollTop(offset - 10)

      $('.ui-jqgrid-hdiv .ui-jqgrid-htable').first().on 'keyup', 'th', (e) ->
        if e.which isnt CONSTANTS.KEYS.TAB
          return
        bodyLeft = $('body').offset().left
        $header = $(e.delegateTarget)
        $body = $('.ui-jqgrid-bdiv')
        headerLeftOffset = bodyLeft - $header.offset().left
        columnOffset = $(this)[0].offsetLeft - headerLeftOffset
        if columnOffset < 330
          $body.scrollLeft(0)
        else
          $body.scrollLeft(headerLeftOffset)
      # update grid max-height on window resize
      $(window).resize () ->
        adjustHeight()

    setSortedColumn: (columns) ->
      sorted = this.options.sort
      return columns if not sorted

      for column in columns
        for item in column['items']
          if sorted.name == item.index
            item.sortorder = sorted.order || 'asc'
        column

    afterLoadComplete: () ->
      this.customizePosition()
      this.highlightSortLabels()

    customizePosition: () ->
      # Move footer row to the top of the table
      $("div.ui-jqgrid-sdiv").insertBefore $("div.ui-jqgrid-bdiv")
      rows = $(".frozen-bdiv .jqgrow")
      $(".frozen-bdiv").css('height', rows.length * 40)
      # ignore students name on tab
      $("#gridWrapper.IAB .ui-jqgrid-bdiv").not(".frozen-bdiv").find("input, a[href!='#']").attr('tabindex', '-1')

    resetFocus: ()->
      $("#{this.lastFocus} a").focus()
      # reset last focus on sorting header
      delete @lastFocus

    render: ()->
      this.renderBody()
      this.renderHeader()
      this.renderFooter()
      this.addARIA()
      this.bindEvents()

    addARIA: ()->
      $('.ui-jqgrid-hdiv .jqg-third-row-header').attr('role', 'row')
      $('.ui-jqgrid-sdiv').attr('aria-label', 'summary')
      $('.ui-jqgrid-bdiv').attr('aria-label', 'body')
      $('#gridTable').removeAttr('aria-labelledby').removeAttr('tabindex').attr('aria-label', 'grid body')
      $('.ui-jqgrid-htable').removeAttr('aria-labelledby')
      $('.jqgfirstrow').attr('aria-hidden', 'true')
      # sorting headers
      $('.jqg-third-row-header .ui-th-ltr').attr('aria-live', 'polite')

    renderBody: () ->
      colNames = this.getColumnNames()
      colModel = this.getColumnModels()
      options = $.extend(this.options,
        colNames: colNames
        colModel: colModel
        # This sets the sort arrows to be shown on sortable columns
        viewsortcols: [true, 'vertical', true]
      )
      this.table.jqGrid options
      this.table.jqGrid "hideCol", "rn"
      this.table.setGridWidth options.defaultWidth, false
      if options.frozenColumns
        this.table.jqGrid('setFrozenColumns').trigger("reloadGrid")

    renderFooter: () ->
      # Add footer row to the grid
      footer = this.footer
      if footer
        this.table.jqGrid('footerData','set', footer, true)
        colum_headers = $('.population-bar-column-header')
        i = 0
        pdf_disable = true
        while i < colum_headers.length
            colum_header = colum_headers[i]
            pdf_disable = pdf_disable && ($(colum_header).data('summative') == false)
            i++
        if $('li.pdf').find('input').attr('disabled') != 'disabled' and pdf_disable
            $('li.pdf').find('input').attr('disabled', 'disabled')
            $('li.pdf'). attr('class','pdf disabled')
        if $('li.extract').find('input').attr('disabled') != 'disabled' and pdf_disable
            $('li.extract').find('input').attr('disabled', 'disabled')
            $('li.extract'). attr('class','extract disabled')

    renderHeader: () ->
      if not this.options.expandableColumns
        return
      headers = this.getHeaders()
      # draw headers
      this.table.jqGrid "setGroupHeaders", {
        useColSpanStyle: true
        groupHeaders: headers
        fixed: true
      }

    getColumnNames: () ->
      columnNames = []
      for column in this.columns
        for item in column['items']
          columnNames.push this.getColumnName(item)
      columnNames

    getColumnModels: () ->
      models = []
      for column in this.columns
        for item in column['items']
          item.parent = column
          models.push this.getColumnModel item
      models

    getColumnModel: (column) ->
      colModelItem =
        name: column.field
        label: column.name
        parentLabel: column.parent?.name
        index: column.index
        width: column.width
        resizable: false # prevent the user from manually resizing the columns

      colModelItem.formatter = (edwareGridFormatters[column.formatter] || column.formatter) if column.formatter
      colModelItem.formatoptions = column.options if column.options
      colModelItem.sorttype = column.sorttype if column.sorttype
      colModelItem.sortable = column.sortable
      colModelItem.align = column.align if column.align
      colModelItem.labels = this.options.labels
      colModelItem.title = column.title
      colModelItem.classes = column.style if column.style
      colModelItem.frozen = column.frozen if column.frozen
      colModelItem.export = column.export
      colModelItem.stickyCompareEnabled = this.options.stickyCompareEnabled
      colModelItem.expanded = if column.expanded then true else false

      #Hide column if the value is true
      if column.hide
        colModelItem.cellattr = (rowId, val, rawObject, cm, rdata) ->
          ' style="display:none;"'
      this.options.sortorder = column.sortorder  if column.sortorder
      this.options.sortname = column.index  if column.sortorder
      colModelItem

    getColumnName: (column) ->
      if column.numberOfColumns and column.expanded isnt 'true' and column.numberOfColumns > 1
        column.displayTpl + EXPAND_ICONS.COLLAPSED
      else
        column.displayTpl

    getHeaders: () ->
      expandedHeaders = []
      cache = {}
      for column in @columns[0].items
        if column.expanded isnt 'true'
          continue
        header =
          startColumnName: column.field
          numberOfColumns: column.numberOfColumns
          titleText: "<div class='expandedHeader' title='#{column.name}'>#{column.name}#{EXPAND_ICONS.EXPANDED}</div>"
        if not cache[column.name]
          expandedHeaders.push(header)
          cache[column.name] = true
      expandedHeaders

    highlightSortLabels: () ->
      sortingHeaders = $('.ui-th-ltr')
      sortingHeaders.removeClass('active')
      grid = $('#gridTable')
      column = grid.jqGrid('getGridParam', 'sortname')
      grid.jqGrid('setLabel', column, '', 'active')
      # highlight frozen column headers
      $('.frozen-div th#gridTable_' + column).addClass('active')
      # highlight expandable column by its name expandable columns has
      # dots and spaces which cannot use jQuery selector to pick it
      # gracefully.
      if column.indexOf("perf_lvl") > 0
        # column name
        columnName = column.split(".")[1]
        $('th[id*="' + columnName + '"]').addClass('active')

    $.fn.edwareGrid = (columns, options, footer) ->
      this.grid = new EdwareGrid(this, columns, options, footer)
      this.grid.render()
      return this.grid

    $.fn.eagerLoad = () ->
      # load all data at once
      this.jqGrid('setGridParam', {scroll: true, rowNum: 100000}).trigger("reloadGrid")

    $.fn.lazyLoad = () ->
      # dynamically load data when scrolling down
      this.jqGrid('setGridParam', {scroll: 1, rowNum: 100}).trigger("reloadGrid")

    $.fn.edwareSortedData = () ->
      # return grid data in sorted order
      grid = this
      sortname = grid.jqGrid('getGridParam', 'sortname')
      sortorder = grid.jqGrid('getGridParam', 'sortorder')
      data = grid.jqGrid('getGridParam', 'data')
      data.sort (row1, row2) ->
        v1 = edwareUtil.deepFind(row1, sortname)
        v2 = edwareUtil.deepFind(row2, sortname)
        if sortorder is 'asc'
          return if v1 > v2 then 1 else -1
        else
          return if v2 > v1 then 1 else -1
      data

  adjustHeight = () ->
    # adjust grid height based on visible region
    $("#gview_gridTable > .ui-jqgrid-bdiv").css {
      'min-height': 100
      'max-height': calculateHeight()
    }

  calculateHeight = () ->
    height = 0
    for component in COMPONENTS_SELECTORS
      $component = $(component)
      height += $component.height() if $component.is(':visible')
    window.innerHeight - height

  beforePrint = () ->
    $('#gridTable').eagerLoad()
    # adjust height to show all rows
    rowHeight = $('.jqgrow').height() + 1 # add 1 for border
    height = $('.jqgrow, .footrow').length * rowHeight
    $("#gview_gridTable > .ui-jqgrid-bdiv").css {
      'height': height
    }

  afterPrint = () ->
    $('#gridTable').lazyLoad()

  createPrintMedia = () ->
    $('#gview_gridTable_print_media').remove()
    gview_gridTable_h = $($('#gview_gridTable .ui-jqgrid-hdiv table').get(0))
    gview_gridTable_b = $($('#gview_gridTable .ui-jqgrid-bdiv table').get(0))
    table_width = gview_gridTable_h.outerWidth()
    page_width =  $('body').width()
    pageCount = Math.ceil(table_width / page_width)
    $('#gridWrapper').append('<div id="gview_gridTable_print_media" class="printContent ui-jqgrid ui-widget ui-widget-content ui-corner-all"></div>')
    printWrap = $('#gview_gridTable_print_media')
    i = 0
    while i < pageCount
      $('<div>&nbsp;</div>').appendTo(printWrap) if i isnt 0
      $('<div class="pageBreak">').appendTo(printWrap) if i isnt 0
      printPage = $('<div class="ui-jqgrid-hbox"></div>').css(overflow: "hidden", width: page_width, "page-break-before": (if i is 0 then "auto" else "always")).appendTo(printWrap)
      if i+1 is pageCount
        printPage.css('margin-bottom', '40px')
      gview_gridTable_h.clone().appendTo(printPage).css({"position": "relative", "left": -i * page_width})
      gview_gridTable_b.clone().appendTo(printPage).css({"position": "relative", "left": -i * page_width})
      i++

  # add hook to run before browser print
  if window.matchMedia
    window.matchMedia('print').addListener (mql)->
      if mql.matches
        beforePrint()
      else
        afterPrint()

  window.onbeforeprint = () ->
    beforePrint()
  window.onafterprint = () ->
    afterPrint()

  #
  #    * Creates EDWARE grid
  #    * @param tableId - The container id for grid
  #    * @param columnItems
  #    * @param columnData
  #    * @param footerData - Grid footer row
  #    * @param options
  #
  create = (config) ->
    # merge configuration
    config = $.extend true, {}, DEFAULT_CONFIG, config
    options = config['options']
    if not options.scroll
      options.rowNum = 100000
    data = config['data']
    options.data = data
    columns = config['columns']
    footer = config['footer']
    if data and data[0]
      edwareUtil.displayErrorMessage ''
      $('#' + config['tableId']).edwareGrid columns, options, footer
    else
      edwareUtil.displayErrorMessage  options.labels['no_results']

  create: create
  adjustHeight: adjustHeight
  createPrintMedia: createPrintMedia
