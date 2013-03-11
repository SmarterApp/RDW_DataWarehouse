define [
  'jquery'
  'jqGrid'
  'cs!EDWARE'
  'cs!edwareUtil'
  'cs!edwarePopulationBar'
], ($, jqGrid, EDWARE, edwareUtil, edwarePopulationBar) ->
  #
  # * EDWARE grid formatters
  # * Handles all the methods for displaying cutpoints, link in the grid
  # 
    
  showlink = (value, options, rowObject) ->
    link = options.colModel.formatoptions.linkUrl
    params = options.colModel.formatoptions.params
    unless rowObject.header
      "<a href=\"" + link + "?"+params.id+"=" + rowObject.student_id + "\">" + $.jgrid.htmlEncode(value) + "</a>"
    else
      "<span class=subTitle2>" + rowObject.subtitle + ":</span><br/><h6>"+value+":</h6>"
  
  showOverallConfidence = (value, options, rowObject) ->
    names = options.colModel.name.split "."
    subject = rowObject[names[0]][names[1]]
    
    "<div>P" + subject.asmt_perf_lvl + " [" + subject.asmt_score_range_min + "] " + value + " [" + subject.asmt_score_range_max + "]</div>"
  
  showClaimsMinMax = (value, options, rowObject) ->
    names = options.colModel.name.split "."
    subject = rowObject[names[0]][names[1]]
   
    "<div>[" + subject[names[2]+ "_range_min"] + "] " + value  + " [" + subject[names[2]+ "_range_max"] + "]</div>"
    
  performanceBar = (value, options, rowObject) ->
    asmt_type = options.colModel.formatoptions.asmt_type
    subject = rowObject.results[asmt_type]
    results = edwarePopulationBar.create subject
    "<div class = 'populationBar'>" + results + "</div>"
 
  showlink: showlink
  showOverallConfidence: showOverallConfidence
  showClaimsMinMax: showClaimsMinMax
  performanceBar: performanceBar