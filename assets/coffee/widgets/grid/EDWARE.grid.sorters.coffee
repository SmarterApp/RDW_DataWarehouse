define [
  'jquery'
  'jqGrid'
], ($, jqGrid) ->

  createPopBarSorter = (index) ->
    return (cell, rowObject) ->
      cell[index]
  
  create: createPopBarSorter
