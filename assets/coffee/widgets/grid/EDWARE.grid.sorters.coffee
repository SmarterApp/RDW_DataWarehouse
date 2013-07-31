define [
  'jquery'
  'jqGrid'
], ($, jqGrid) ->

  popBarSort = (cell, rowObject) ->
    checked = $('.inputColorBlock:checked')
    if checked
      subject = checked.data('subject')
      index = checked.data('index')
      value = -1
      for result of rowObject.results
        cur = rowObject.results[result]
        if cur.asmt_subject == subject
          value = cur.sort[index]
          break
      value
    else
      ""
  
  popBarSort:popBarSort
