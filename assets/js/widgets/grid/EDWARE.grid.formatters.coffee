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
  
  showOverallConfidence = (value, options, rowObject) ->
    names = options.colModel.name.split "."
    subject = rowObject[names[0]][names[1]]
    
    "<div>P" + subject.asmt_perf_lvl + " [" + subject.asmt_score_range_min + "] " + value + " [" + subject.asmt_score_range_max + "]</div>"
  
  showClaimsMinMax = (value, options, rowObject) ->
    names = options.colModel.name.split "."
    subject = rowObject[names[0]][names[1]]
   
    "<div>[" + subject[names[2]+ "_min"] + "] " + value  + " [" + subject[names[2]+ "_max"] + "]</div>"
 
  showlink: showlink
  showOverallConfidence: showOverallConfidence
  showClaimsMinMax: showClaimsMinMax