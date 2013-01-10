generate_ticks = (json_data) ->
  scope_groups = json['scope_groups'][0]
  grade_groups = scope_groups['grade_groups'][0]
  bar_groups = grade_groups['bar_groups'][0]
  bars = bar_groups['bars']

generate_jqplot_input = (json_data) ->
  scope_groups = json_data['scope_groups'][0]
  grade_groups = scope_groups['grade_groups'][0]
  bar_groups = grade_groups['bar_groups'][0]
  bars = bar_groups['bars']

  seg_list = generate_seg_list(bars)

  # Most sources say to avoid indexing an array like this
  # They recommend using iterators and list comprehension to perform actions like this
  # TODO: come back and re-do this using list comprehension (if possible)
  for bar in bars
    segs = bar['segments']
    for i in [0..(segs.length - 1)]
      current_seg = segs[i]
      seg_list[i].push(current_seg['student_percentage'])
  seg_list

generate_seg_list = (bars) ->
  num_segs = get_number_of_segments(bars)
  seg_list = [] for i in [1..num_segs]

get_number_of_segments = (bars) ->
  try
    num_segs = bars[0]['segments'].length
    for bar in bars
      if (num_segs != bar['segments'].length)
        throw 'Different bars have different number of segments'
  catch error
    console.log('Malformed "bars" list, malformed "segments" list, or different number of segments')
  num_segs

$(document).ready ->

  #$("#json_string").html(JSON.stringify(json_data));

  #$.jqplot('chart',  [[[1, 2],[3,5.12],[5,13.1],[7,33.6],[9,85.9],[11,219.9]]]);

  jqplot_input = generate_jqplot_input(json_data)
  #ticks = generate_ticks(json_data)

  plot_test = $.jqplot('chart_test', jqplot_input, {
    # Tell the plot to stack the bars.
    stackSeries: true,
    captureRightClick: true,
    seriesDefaults: {
      renderer: $.jqplot.BarRenderer,
      rendererOptions: {
        # Put a 30 pixel margin between bars.
        barMargin: 30,
        # Highlight bars when mouse button pressed.
        # Disables default highlighting on mouse over.
        highlightMouseDown: true,
        barDirection: 'horizontal'
      },
      pointLabels: {show: true}
    },
    axes: {
      xaxis: {
        max:100
      },
      yaxis: {
        # Don't pad out the bottom of the data range.  By default,
        # axes scaled as if data extended 10% above and below the
        # actual range to prevent data points right on grid boundaries.
        # Don't want to do that here.
        padMin: 0,
        renderer: $.jqplot.CategoryAxisRenderer,
        ticks: ['School 1', 'School 2', 'School 3']
      }
    },
    legend: {
      show: false,
      location: 'e',
      placement: 'outside'
    }
  })


  # Bind a listener to the "jqplotDataClick" event.  Here, simply change
  # the text of the info element to show what series and ponit were
  # clicked along with the data for that point.

  callback =  (ev, seriesIndex, pointIndex, data) ->
    $('#info').html('series: ' + seriesIndex + ', point: ' + pointIndex + ', data: ' + data)

  $('#chart').bind('jqplotDataClick', callback)

  $('#chart_test').bind('jqplotDataClick', callback)