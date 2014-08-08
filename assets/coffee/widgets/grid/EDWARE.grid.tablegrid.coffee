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
      rowNum: 100
      gridview: true
      scroll: 1
      shrinkToFit: false
      defaultWidth: 980
      loadComplete: () ->

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
      $('.ui-jqgrid-sortable').click ()->
        lastFocus = "##{this.id}"
        # escape dot in element id
        self.lastFocus = lastFocus.replace(/\./gi, '\\.')
        # emit sorting event to other listeners
        $(document).trigger CONSTANTS.EVENTS.SORT_COLUMNS

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

    setSortedColumn: (columns) ->
      sorted = this.options.sort
      return columns if not sorted

      for column in columns
        for item in column['items']
          if sorted.name == item.index
            item.sortorder = sorted.order || 'asc'
        column

    afterLoadComplete: () ->
      # Move footer row to the top of the table
      $("div.ui-jqgrid-sdiv").insertBefore $("div.ui-jqgrid-bdiv")
      this.highlightSortLabels()

    resetFocus: ()->
      $("#{this.lastFocus} a").focus()
      # reset last focus on sorting header
      delete @lastFocus

    render: ()->
      this.renderBody()
      this.renderHeader()
      this.renderFooter()
      # this.renderPrintHeader()
      this.addARIA()
      this.bindEvents()

    renderPrintHeader: ()->
      # set repeating headers
      $gridTable = $("div.ui-jqgrid-bdiv table")
      $gridTable.prepend $('.ui-jqgrid-hdiv thead').clone()
      # $gridTable.prepend $('.ui-jqgrid-sdiv .footrow').clone()

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

    renderFooter: () ->
      # Add footer row to the grid
      footer = this.footer
      this.table.jqGrid('footerData','set', footer, true) if footer

    renderHeader: () ->
      headers = this.getHeaders()
      return if headers.length <= 0
      # draw headers
      this.table.jqGrid "setGroupHeaders", {
        useColSpanStyle: false
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
        parentLabel: column.parent.name
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

      #Hide column if the value is true
      if column.hide
        colModelItem.cellattr = (rowId, val, rawObject, cm, rdata) ->
          ' style="display:none;"'
      this.options.sortorder = column.sortorder  if column.sortorder
      this.options.sortname = column.index  if column.sortorder
      colModelItem

    getColumnName: (column) ->
      column.displayTpl

    getHeaders: () ->
      for column in this.columns
        startColumnName: column.items[0].field
        numberOfColumns: column.items.length
        titleText: column.name

    highlightSortLabels: () ->
      sortingHeaders = $('.jqg-third-row-header .ui-th-ltr')
      sortingHeaders.removeClass('active')
      grid = $('#gridTable')
      column = grid.jqGrid('getGridParam', 'sortname')
      grid.jqGrid('setLabel', column, '', 'active')

    $.fn.edwareGrid = (columns, options, footer) ->
      this.grid = new EdwareGrid(this, columns, options, footer)
      this.grid.render()

      # trigger gridComplete event
      options.gridComplete() if options.gridComplete
      return this.grid

    $.fn.eagerLoad = () ->
      # load all data at once
      this.jqGrid('setGridParam', {scroll: false, rowNum: 100000}).trigger("reloadGrid")

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
      'height': calculateHeight()
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
    data = config['data']
    # options.data = data
    for i in [1..2]
      data = data.concat(data)
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
