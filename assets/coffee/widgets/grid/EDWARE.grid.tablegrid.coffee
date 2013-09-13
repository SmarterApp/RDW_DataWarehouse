define [
  'jquery'
  'jqGrid'
  'edwareUtil'
  'edwareGridFormatters'
  'edwareGridSorters'  
], ($, jqGrid, edwareUtil, edwareGridFormatters, edwareGridSorters) ->
  #
  # * EDWARE grid
  # * The module contains EDWARE grid plugin and grid creation method
  # 
    
    #
    #    *  EDWARE Grid plugin
    #    *  @param panelConfig - Panel config data
    #    *  @param options
    #    *  Example: $("#table1").edwareGrid(columnItems, gridOptions)
    #    
    
    (($) ->
      $.fn.edwareGrid = (columns, options, footerData) ->
        colNames = []
        colModel = []
        groupHeaders = []
        for item, i in columns
          if item.items and item.items.length > 0
            items = item.items
            groupHeaders.push
              startColumnName: item.items[0].field
              numberOfColumns: item.items.length
              titleText: item.name
          else
            items = [item]

          for item1, j in items
            colNames.push item1.name
            colModelItem =
              name: item1.field
              index: item1.index
              width: item1.width

            colModelItem.formatter = (edwareGridFormatters[item1.formatter] || item1.formatter)  if item1.formatter
            colModelItem.formatoptions = item1.options  if item1.options
            colModelItem.sorttype = item1.sorttype if item1.sorttype
            colModelItem.sortable = item1.sortable
            colModelItem.align = item1.align  if item1.align
            colModelItem.labels = options.labels if options.labels

            if item1.title isnt undefined
              colModelItem.title = item1.title

            colModelItem.classes = item1.style  if item1.style
            colModelItem.frozen = item1.frozen  if item1.frozen

            # Hide column if the value is true
            if item1.hide
              colModelItem.cellattr = (rowId, val, rawObject, cm, rdata) ->
                ' style="display:none;"'
            options.sortorder = item1.sortorder  if item1.sortorder
            options.sortname = item1.index  if item1.sortorder
            colModelItem.resizable = false # prevent the user from manually resizing the columns
            colModel.push colModelItem

          options = $.extend(options,
            colNames: colNames
            colModel: colModel
            onSortCol: (index, idxcol, sortorder) ->
              # show the icons of last sorted column
              $(@grid.headers[@p.lastsort].el).find(">div.ui-jqgrid-sortable>span.s-ico").show()  if @p.lastsort >= 0 and @p.lastsort isnt idxcol and @p.colModel[@p.lastsort].sortable isnt false
          )
        this.jqGrid options
        this.jqGrid "hideCol", "rn"
        this.setGridWidth 980, false

        colModel = $(this).jqGrid("getGridParam", "colModel")
        $("#gbox_" + $.jgrid.jqID($(this)[0].id) + " tr.ui-jqgrid-labels th.ui-th-column").each (i) ->
          cmi = colModel[i]
          colName = cmi.name
          if cmi.sortable isnt false
            
            # show the sorting icons
            $(this).find(">div.ui-jqgrid-sortable>span.s-ico").show()
          
          # change the mouse cursor on the columns which are non-sortable
          else $(this).find(">div.ui-jqgrid-sortable").css cursor: "default"  if not cmi.sortable and colName isnt "rn" and colName isnt "cb" and colName isnt "subgrid"


        if groupHeaders.length > 0
          $(this).jqGrid "setGroupHeaders",
            useColSpanStyle: false
            groupHeaders: groupHeaders
            fixed: true
        
        # Add footer row to the grid
        if footerData
          $(this).jqGrid('footerData','set', footerData, true);
     

      $.fn.edwareGrid.DEFAULT_CONFIG =
        tableId: 'gridTable'
        data: undefined
        options:
          gridHeight: window.innerHeight * 0.6 #default grid height
          datatype: "local"
          height: "auto"
          viewrecords: true
          autoencode: true
          rowNum: 10000
          shrinkToFit: false
          loadComplete: () ->


      $.fn.sortBySubject = (subject, index, order) ->
        order = order || 'asc'
        colModels = this.jqGrid("getGridParam", "colModel");
        if subject != 'name' and colModels != undefined
          for colModel in colModels
            colModel.sorttype = edwareGridSorters.create(index) if colModel.index == subject
        this.sortGrid(subject, true, order)

    ) jQuery

    #
    #    * Creates EDWARE grid
    #    * @param tableId - The container id for grid
    #    * @param columnItems
    #    * @param columnData
    #    * @param footerData - Grid footer row 
    #    * @param options
    #    
    create = (($) -> 
      return (config) ->
        # tableId, columnItems, columnData, footerData, options
        # columnData = config['data'][columnItems.root]
        # merge configuration
        config = $.extend {}, $.fn.edwareGrid.DEFAULT_CONFIG, config
        options = config['options']
        data = config['data']
        columns = config['columns']
        footer = config['footer']
        if not data
          edwareUtil.displayNoResultsMessage()
          return
        options.data = data
        options.footerrow = true if config['footer']
        options.loadComplete = () ->
          # Move footer row to the top of the table
          $("div.ui-jqgrid-sdiv").insertBefore $("div.ui-jqgrid-bdiv")
          $("#gview_gridTable > .ui-jqgrid-bdiv").css {
              'min-height': 100, 'height': options.gridHeight
          }

        #TODO edwareUtil.displayErrorMessage ""
        $("#" + config['tableId']).edwareGrid columns, options, footer
      ) jQuery
        
    create: create
    
