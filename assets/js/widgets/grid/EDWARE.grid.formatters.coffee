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
    unless value is "Overall Summary"
      "<a href=\"" + link + "?"+params.id+"=" + rowObject.student_id + "\">" + $.jgrid.htmlEncode(value) + "</a>"
    else
      "<span class=subTitle2>Reference Point:</span><br/><h6>"+value+":</h6>"
  
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
    intervals = subject.intervals
    defaultColors =
        0:
          bg_color: "#DD514C"
          start_gradient_bg_color: "#EE5F5B"
          end_gradient_bg_color: "#C43C35"
          text_color: "#FFFFFF"
      
        1:
          bg_color: "#e4c904"
          start_gradient_bg_color: "#e3c703"
          end_gradient_bg_color: "#eed909"
          text_color: "#000"
      
        2:
          bg_color: "#3b9f0a"
          start_gradient_bg_color: "#3d9913"
          end_gradient_bg_color: "#65b92c"
          text_color: "#FFFFFF"
      
        3:
          bg_color: "#237ccb"
          start_gradient_bg_color: "#2078ca"
          end_gradient_bg_color: "#3a98d1"
          text_color: "#FFFFFF"
        
    i = 0
    len = intervals.length
    # For now, ignore everything behind the 4th interval
    if len > 4
      intervals = intervals[0..3]
      len = intervals.length
    while (i < len)
      element = intervals[i]
      element.color = defaultColors[i]
      i++
    subject.intervals = intervals
    results = edwarePopulationBar.create subject
    unless rowObject.headerRow
      "<div class = 'populationBar'>" + results + "</div>"+ rowObject['results'][""+asmt_type+""].total
    else
      "<div class = 'populationBar'>" + results + "</div>"+ rowObject['results'][""+asmt_type+".total"]
 
  showlink: showlink
  showOverallConfidence: showOverallConfidence
  showClaimsMinMax: showClaimsMinMax
  performanceBar: performanceBar