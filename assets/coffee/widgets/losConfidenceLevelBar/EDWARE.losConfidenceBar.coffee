#global define
define [
  "jquery"
  "mustache"
  "text!edwareLOSConfidenceLevelBarTemplate"
], ($, Mustache, losConfidenceLevelBarTemplate) ->

  # score indicator image width
  SCORE_INDICATOR_WIDTH = 5

  #
  #    * Performance bar widget for student list report
  #    * Generate error band bar and calculate cutpoint pixel width, score position, score interval position
  #    * @param items - data for the confidence level bar
  #    * @param barWidth - Width of the bar in pixel
  #
  $.fn.losConfidenceLevelBar = (items, barWidth) ->

    score_range =  items.asmt_score_max - items.asmt_score_min

    prev_cut_point = { interval: items.asmt_score_min }

    for cut_point_interval in items.cut_point_intervals
      cut_point_interval.asmt_cut_point =  ((cut_point_interval.interval - prev_cut_point.interval) / score_range) * barWidth
      prev_cut_point = cut_point_interval

    # Calculate position for dot indicator
    score_pos = Math.round(((items.asmt_score - items.asmt_score_min) / score_range) * barWidth) - (SCORE_INDICATOR_WIDTH / 2)
    score_pos = barWidth if score_pos >= barWidth

    # calculate error band mininum range
    errorband_min_range = Math.round((((items.asmt_score - items.asmt_score_min - items.asmt_score_interval) / score_range) * barWidth)) - 2

    # calculate error band maximum range
    errorband_max_range = Math.round((((items.asmt_score - items.asmt_score_min) + items.asmt_score_interval) / score_range) * barWidth)

    # Set pixel width of error band
    errorband_width = errorband_max_range - errorband_min_range
    errorband_width = 5 if errorband_width <= 5

    # Adjust score dot marker and error band if score is at the edege of the bar.
    errorband_min_range = barWidth - 2 if errorband_min_range >= barWidth - 2

    cutLine = calculateCutLineForSwimLane(items.cut_point_intervals, errorband_min_range, errorband_max_range)

    # use mustache template to display the json data
    output = Mustache.to_html losConfidenceLevelBarTemplate, {
      bar_width: barWidth
      asmt_score_pos: score_pos
      asmt_errorband_width: errorband_width
      asmt_errorband_min_range: errorband_min_range
      cutLine: cutLine
      cut_point_intervals: items.cut_point_intervals
    }

    if this.length > 0
      this.html output
    else
      return output

  calculateCutLineForSwimLane = (cut_point_intervals, lowerBound, upperBound) ->
    interval = 0
    for cut_point_interval, idx in cut_point_intervals
      # do not show cut line for last interval
      break if idx is cut_point_intervals.length - 1
      interval = interval + cut_point_interval.asmt_cut_point
      if lowerBound <= interval <= upperBound
        return interval - lowerBound - (idx + 1) # subtract borders
    return -999

  create = (data, barWidth, containerId) ->
    $(containerId).losConfidenceLevelBar data, barWidth

  create: create
