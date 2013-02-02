define [
  'jquery'
  'jqGrid'
  'cs!EDWARE'
  'cs!edwareUtil'
], ($, jqGrid, EDWARE, edwareUtil) ->
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
    util = edwareUtil
    
    (($) ->
      $.fn.edwareGrid = (panelConfig, options) ->
        colNames = []
        colModel = []
        groupHeaders = []
        if panelConfig
          i = 0
          while i < panelConfig.length
            item = panelConfig[i]
            if item.items and item.items.length > 0
              items = item.items
              groupHeaders.push
                startColumnName: item.items[0].field
                numberOfColumns: item.items.length
                titleText: item.name
            
            else
              items = [item]
              
            j = 0
            while j < items.length
              
              item1 = items[j]
              colNames.push item1.name
              colModelItem =
                name: item1.field
                index: item1.field
                width: item1.width
  
              colModelItem.align = item1.align  if item1.align
              colModelItem.classes = item1.style  if item1.style
              colModelItem.resizable = false # prevent the user from manually resizing the columns
              colModel.push colModelItem
              j++
              
            i++
          options = $.extend(options,
            colNames: colNames
            colModel: colModel
          )
        $(this).jqGrid options
        $(this).jqGrid "hideCol", "rn"
        
        if groupHeaders.length > 0
          $(this).jqGrid "setGroupHeaders",
            useColSpanStyle: false
            groupHeaders: groupHeaders
            fixed: true
            
        $(this).find(".jqg-second-row-header th:first-child").css "background", "#ffffff"
        
    ) jQuery
    
    #
    #    * Creates EDWARE grid
    #    * @param tableId - The container id for grid
    #    * @param columnItems
    #    * @param columnData
    #    * @param assessmentCutpoints
    #    * @param options
    #    
    create = (tableId, columnItems, columnData, assessmentCutpoints, options) ->
      
      columnData = columnData[columnItems.root]  if columnItems.root and columnData isnt null and columnData isnt `undefined`
      
      gridOptions =
        data: columnData
        datatype: "local"
        height: "auto"
        viewrecords: true
        autoencode: true
        rowNum: 10000
        loadComplete: ->
           $("tr.jqgrow:odd").css "background", "#f8f8f8"
  
      if columnData is null or columnData is `undefined` or columnData.length < 1
        util.displayErrorMessage "There is no data available for your request. Please contact your IT administrator."
      else
        gridOptions = $.extend(gridOptions, options)  if options
        $("#" + tableId).edwareGrid columnItems, gridOptions
        
    create: create