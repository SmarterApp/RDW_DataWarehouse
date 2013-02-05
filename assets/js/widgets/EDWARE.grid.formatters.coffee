define [
  'jquery'
  'jqGrid'
  'cs!EDWARE'
  'cs!edwareUtil'
], ($, jqGrid, EDWARE, edwareUtil) ->
  #
  # * EDWARE grid formatters
  # * Handles all the methods for displaying cutpoints, link in the grid
  # 
    
  showlink = (value, options, rowObject) ->
    link = options.colModel.formatoptions.linkUrl
    "<a href=\"" + link + "?studentId=" + rowObject.student_id + "\">" + $.jgrid.htmlEncode(value) + "</a>"
  
  showlink: showlink
    
  