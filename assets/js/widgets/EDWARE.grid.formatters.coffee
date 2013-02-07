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
  
  showConfidenceRange = (value, options, rowObject) ->
    subjectType = options.colModel.formatoptions.type.toLowerCase()
    if subjectType == 'math'
      subject = rowObject.assessments.MATH
    else if subjectType == 'ela'
      subject = rowObject.assessments.ELA
   
    "<div>P" + subject.asmt_perf_lvl + " [" + subject.asmt_score_range_min + "] " + value + " [" + subject.asmt_score_range_max + "]</div>"
  
  showlink: showlink
  showConfidenceRange: showConfidenceRange