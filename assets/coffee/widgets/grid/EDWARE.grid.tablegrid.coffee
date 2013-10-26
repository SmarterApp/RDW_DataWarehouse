define [
  'jquery'
  'jqGrid'
  'edwareUtil'
  'edwareGridFormatters'
  'edwareGridSorters'  
], ($, jqGrid, edwareUtil, edwareGridFormatters, edwareGridSorters) ->

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

    setSortedColumn: (columns) ->
      sorted = this.options.sort
      return columns if not sorted
      
      for column in columns
        if sorted.name == column.items[0].index
          column.items[0].sortorder = sorted.order || 'asc'
          column.items[0].sorttype = edwareGridSorters.create(sorted.index) if sorted.name != 'name'
        column

    afterLoadComplete: () ->
      # Move footer row to the top of the table
      $("div.ui-jqgrid-sdiv").insertBefore $("div.ui-jqgrid-bdiv")
      $("#gview_gridTable > .ui-jqgrid-bdiv").css {
          'min-height': 100, 'height': this.options.gridHeight
      }

    render: ()->
      this.renderBody()
      this.renderHeader()
      this.renderFooter()

    renderBody: () ->
      colNames = this.getColumnNames()
      colModel = this.getColumnModels()
      options = $.extend(this.options,
        colNames: colNames
        colModel: colModel
        onSortCol: (index, idxcol, sortorder) ->
          #TODO show the icons of last sorted column
          $(@grid.headers[@p.lastsort].el).find(">div.ui-jqgrid-sortable>span.s-ico").show()  if @p.lastsort >= 0 and @p.lastsort isnt idxcol and @p.colModel[@p.lastsort].sortable isnt false
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
          models.push this.getColumnModel item 
      models
      
    getColumnModel: (column) ->
      colModelItem =
        name: column.field
        label: column.name
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
      column.name + column.displayTpl

    getHeaders: () ->
      for column in this.columns
        startColumnName: column.items[0].field
        numberOfColumns: column.items.length
        titleText: column.name


    $.fn.edwareGrid = (columns, options, footer) ->
      this.grid = new EdwareGrid(this, columns, options, footer)
      this.grid.render()
      # trigger gridComplete event
      options.gridComplete() if options.gridComplete

      colModel = $(this).jqGrid("getGridParam", "colModel")
      $("#gbox_" + $.jgrid.jqID($(this)[0].id) + " tr.ui-jqgrid-labels th.ui-th-column").each (i) ->
        cmi = colModel[i]
        colName = cmi.name
        if cmi.sortable isnt false

          # show the sorting icons
          $(this).find(">div.ui-jqgrid-sortable>span.s-ico").show()

        # change the mouse cursor on the columns which are non-sortable
        else $(this).find(">div.ui-jqgrid-sortable").css cursor: "default"  if not cmi.sortable and colName isnt "rn" and colName isnt "cb" and colName isnt "subgrid"

    $.fn.sortBySubject = (subject, index, order) ->
      order = order || 'asc'
      colModels = this.getGridParam('colModel')
      if subject != 'name'
        for colModel in colModels
          colModel.sorttype = edwareGridSorters.create(index) if colModel.index == subject
      this.sortGrid(subject, true, order)

    $.fn.eagerLoad = () ->
      # load all data at once
      this.jqGrid('setGridParam', {scroll: false, rowNum: 100000}).trigger("reloadGrid")

    $.fn.lazyLoad = () ->
      # dynamically load data when scrolling down
      this.jqGrid('setGridParam', {scroll: 1, rowNum: 100}).trigger("reloadGrid")
      
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
    options.data = data
    columns = config['columns']
    footer = config['footer']
    if data and data[0]
      edwareUtil.displayErrorMessage ''
      $('#' + config['tableId']).edwareGrid columns, options, footer
    else
      edwareUtil.displayErrorMessage  options.labels['no_results']
      
  create: create
    
