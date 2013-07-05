define [
  'jquery'
  'jqGrid'
  'edwareUtil'
], ($, jqGrid, edwareUtil) ->

  popBarSort = (cell, rowObject) ->
    checked = $('.inputColorBlock:checked').val()
    if checked
      subject = checked.substring(0, checked.indexOf('_'))
      index = $('#' + checked ).index()
      
      for result of rowObject.results
        cur = rowObject.results[result]
        if cur.asmt_subject == subject
          value = cur.sort[index]
          break
      
      # Set/reset bar alignment as per the alignment status
      edwareUtil.formatBarAlignment() 
      value
    else
      null
      

  
  popBarSort:popBarSort
