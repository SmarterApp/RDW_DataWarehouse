generate_jqplot_input = (json) ->
  scope_groups = json['scope_groups'][0]
  grade_groups = scope_groups['grade_groups'][0]
  bar_groups = grade_groups['bar_groups'][0]
  bars = bar_groups['bars']

  num_segs = get_number_of_segments(bars)
  console.log(num_segs)

  bar_list = []
  for bar in bars
    seg_list = []
    for seg in bar['segments']
      seg_list.push(seg['student_count'])
    bar_list.push(seg_list)

  prepare_list_for_jqplot(bar_list)

prepare_list_for_jqplot = (bar_list) ->
  



get_number_of_segments = (bars) ->
  first_bar = bars[0]
  first_bar['segments'].length

$(document).ready ->

  #$("#json_string").html(JSON.stringify(json_data));

  #$.jqplot('chart',  [[[1, 2],[3,5.12],[5,13.1],[7,33.6],[9,85.9],[11,219.9]]]);

  scope_groups = generate_jqplot_input(json_data)

  s1 = [2, 6, 7, 10];
  s2 = [7, 5, 3, 4];
  s3 = [14, 9, 3, 8];

  plot3 = $.jqplot('chart', [s1, s2, s3], {
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
        highlightMouseDown: true
        },
      pointLabels: {show: true}
      },
    axes: {
      xaxis: {
        renderer: $.jqplot.CategoryAxisRenderer
      },
      yaxis: {
        # Don't pad out the bottom of the data range.  By default,
        # axes scaled as if data extended 10% above and below the
        # actual range to prevent data points right on grid boundaries.
        # Don't want to do that here.
        padMin: 0
      }
    },
    legend: {
      show: false,
      location: 'e',
      placement: 'outside'
      }
  });

  # Bind a listener to the "jqplotDataClick" event.  Here, simply change
  # the text of the info element to show what series and ponit were
  # clicked along with the data for that point.

  callback =  (ev, seriesIndex, pointIndex, data) ->
    $('#info').html('series: ' + seriesIndex + ', point: ' + pointIndex + ', data: ' + data);

  $('#chart').bind('jqplotDataClick', callback);