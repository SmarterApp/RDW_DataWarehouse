#global define
define [
  "jquery"
  "mustache"
  "text!edwareLOSConfidenceLevelBarTemplate"
], ($, Mustache, losConfidenceLevelBarTemplate) ->
   
  #
  #    * Performance bar widget for student list report
  #    * Generate error band bar and calculate cutpoint pixel width, score position, score interval position
  #    * @param items - data for the confidence level bar
  #    * @param barWidth - Width of the bar in pixel
  #    
  $.fn.losConfidenceLevelBar = (items, barWidth) ->
      
      #Total bar width
      items.bar_width = barWidth
      #score indicator image width
      score_indicator_width = 5
      
      # Last cut point of the assessment
      items.last_interval = items.cut_point_intervals[items.cut_point_intervals.length-1]
      
      items.score_min_max_difference =  items.asmt_score_max - items.asmt_score_min
      
      # Calculate width for first cutpoint
      items.cut_point_intervals[0].asmt_cut_point =  ((items.cut_point_intervals[0].interval - items.asmt_score_min) / items.score_min_max_difference) * items.bar_width
      
      # Calculate width for last cutpoint
      items.last_interval.asmt_cut_point =  ((items.last_interval.interval - items.cut_point_intervals[items.cut_point_intervals.length-2].interval) / items.score_min_max_difference) * items.bar_width
      
      # Calculate width for cutpoints other than first and last cutpoints
      j = 1     
      while j < items.cut_point_intervals.length - 1
        items.cut_point_intervals[j].asmt_cut_point =  ((items.cut_point_intervals[j].interval - items.cut_point_intervals[j-1].interval) / items.score_min_max_difference) * items.bar_width
        j++
      
      # Calculate position for dot indicator
      items.asmt_score_pos = Math.round(((items.asmt_score - items.asmt_score_min) / items.score_min_max_difference) * items.bar_width) - (score_indicator_width / 2)
      
      # calculate error band mininum range
      items.asmt_errorband_min_range = Math.round((((items.asmt_score - items.asmt_score_min - items.asmt_score_interval) / items.score_min_max_difference) * items.bar_width)) - 2
      
      # calculate error band maximum range
      items.asmt_errorband_max_range = Math.round((((items.asmt_score - items.asmt_score_min) + items.asmt_score_interval) / items.score_min_max_difference) * items.bar_width) 
      
      # Set pixel width of error band
      items.asmt_errorband_width = items.asmt_errorband_max_range - items.asmt_errorband_min_range
      
      # Adjust score dot marker and error band if score is at the edege of the bar.
      items.asmt_errorband_width = 5 if items.asmt_errorband_width <= 5            
      items.asmt_errorband_min_range = barWidth - 2 if items.asmt_errorband_min_range >= barWidth - 2        
      items.asmt_score_pos = barWidth if items.asmt_score_pos >= barWidth
      
      # use mustache template to display the json data  
      output = Mustache.to_html losConfidenceLevelBarTemplate, items 
        
      if this.length > 0
        this.html output
      else
        return output
      
      
  create = (data, barWidth, containerId) ->
    
     $(containerId).losConfidenceLevelBar data, barWidth

  create: create