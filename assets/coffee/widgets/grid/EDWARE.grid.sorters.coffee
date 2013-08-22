define [
  'jquery'
  'jqGrid'
], ($, jqGrid) ->

  popBarSort = (cell, rowObject) ->
    index = $('.inputColorBlock:checked').data('index')
    cell[index]
  
  popBarSort:popBarSort
