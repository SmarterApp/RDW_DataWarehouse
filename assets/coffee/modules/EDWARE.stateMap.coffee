require [
  'jquery'
  'raphael'
  'usmap'
  'edwareDataProxy'
  'edwareUtil'
  'edwareHeader'
  'edwareBreadcrumbs'
], ($, Raphael, usmap, edwareDataProxy, edwareUtil, edwareHeader, edwareBreadcrumbs) ->

  state_label_pos = 
    VT:
      name:
        x: 800
        y: 75
      line:
        x1: 825
        y1: 75
        x2: 840
        y2: 100
    NH:
      name:
        x: 835
        y: 65
      line:
        x1: 850
        y1: 73
        x2: 862
        y2: 90
    CT:
      name:
        x: 870
        y: 210
      line:
        x1: 869
        y1: 210
        x2: 862
        y2: 187
    DE:
      name:
        x: 845
        y: 275
      line:
        x1: 843
        y1: 274
        x2: 830
        y2: 256
    MA:
      name:
        x: 900
        y: 145
      line:
        x1: 900
        y1: 145
        x2: 885
        y2: 159
    RI:
      name:
        x: 900
        y: 190
      line:
        x1: 898
        y1: 185
        x2: 878
        y2: 178
    NJ:
      name:
        x: 860
        y: 235
      line:
        x1: 858
        y1: 232
        x2: 844
        y2: 220
    MD:
      name:
        x: 840
        y: 300
      line:
        x1: 840
        y1: 300
        x2: 830
        y2: 275
    DC:
      name:
        x: 850
        y: 255
      line:
        x1: 850
        y1: 255
        x2: 805
        y2: 250

  edwareDataProxy.getDataForReport('comparingPopulationsReport').done (reportConfig) ->
      options =
        method: 'POST'
      load = edwareDataProxy.getDatafromSource "/services/userinfo", options
      load.done (data) ->
        stateCodes = edwareUtil.getUserStateCode data.user_info
        stateCodes = stateCodes.concat ['WA', 'OR', 'ID', "NV", "MT", 'WY', 'ND', 'SD', 'CT', 'VT', 'NY', 'DE', 'SC', 'AK', "HI", "ME"]
        #TODO: maybe move to less file
        stateColor = '#0085ad'
        stateHoverColor = '#43b02a'
        stateStyleMap = {}
        stateHoverMap = {}
        stateStyles = {
          fill: '#3fa3c1'
          stroke: '#ffffff'
          'stroke-width': .10
        }

        # Add text for header string
        # $('#titleString').append('<text>Select State to start exploring Smarter Balanced test results</h2>')

        for stateCode in stateCodes
          stateStyleMap[stateCode] = 'fill': stateColor
          stateHoverMap[stateCode] = 'fill': stateHoverColor

        $('#map').usmap {
          showLabels: true
          stateStyles: stateStyles
          stateHoverStyles: fill: '#3fa3c1'
          stateHoverAnimation: 100
          stateSpecificStyles: stateStyleMap
          stateSpecificHoverStyles: stateHoverMap
          click: (event, data) ->
            if data.name in stateCodes
              window.location.href = window.location.protocol + "//" + window.location.host + "/assets/html/comparingPopulations.html?stateCode=" + data.name
        }

        
        #Removes the state codes that are added by usmap
        $('#map svg text tspan').each () ->
          if this.firstChild.data not in stateCodes or this.firstChild.data of state_label_pos
            this.firstChild.data = ''

        rem_x = []
        rem_y = []
        # Remove small state text boxes drawn by usmap.js
        $('#map svg rect').each () ->
          if $(this).attr('fill')  == "#333333"
            rem_x.push $(this).attr('x')
            rem_y.push $(this).attr('y')
            $(this).hide()

        i = 0
        while i < rem_x.length
          x = rem_x[i]
          y = rem_y[i]
          $('#map svg text, #map svg rect').each () ->
            if $(this).attr('x') == x and $(this).attr('y') == y
              $(this).hide()
          ++i

        for state_code, coord of state_label_pos
          if state_code in stateCodes
            st_txt = $('<text></text>')
            st_txt.attr(coord.name)
            st_span = $('<tspan dy="5.682005882263184"></tsapn')
            st_span.append(state_code)
            st_txt.append(st_span)
            $('#map svg').append(st_txt)

            st_line = $('<line></line>')
            st_line.attr(coord.line)
            $('#map svg').append(st_line)        

        edwareHeader.create(data, reportConfig)
        displayHome = edwareUtil.getDisplayBreadcrumbsHome data.user_info
        $('#breadcrumb').breadcrumbs(data.context, reportConfig.breadcrumb, displayHome)

        # refresh html of map div to display newly added labels
        $('#map').html($('#map').html())
