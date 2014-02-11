require [
  'jquery'
  'raphael'
  'usmap'
  'edwareDataProxy'
  'edwareUtil'
  'edwareHeader'
  'edwareBreadcrumbs'
], ($, Raphael, usmap, edwareDataProxy, edwareUtil, edwareHeader, edwareBreadcrumbs) ->

  SVG = (tag) ->
    document.createElementNS('http://www.w3.org/2000/svg', tag)

  edwareDataProxy.getDataForReport('stateMap').done (stateMapConfig) ->
      options =
        method: 'POST'
      load = edwareDataProxy.getDatafromSource "/services/userinfo", options
      load.done (data) ->
        stateCodes = edwareUtil.getUserStateCode data.user_info
        # stateCodes = stateCodes.concat ['WA', 'OR', 'ID', "NV", "MT", 'WY', 'ND', 'SD', 'CT', 'VT', 'NY', 'DE', 'SC', 'AK', "HI", "ME", "NH", "WV", 'KS', 'PA', 'NC', 'MI', 'WI', 'IA', 'MO', "MA", 'RI', 'NJ', 'MD', 'DC']
        
        # get colors from report
        colors = stateMapConfig.colors

        stateStyleMap = {}
        stateHoverMap = {}
        stateStyles = 
          fill: colors.defaultFill
          stroke: colors.defaultStroke
          'stroke-width': colors.strokeWidth

        # add fill and hover for each state in the list
        for stateCode in stateCodes
          stateStyleMap[stateCode] = 'fill': colors.stateStyle
          stateHoverMap[stateCode] = 'fill': colors.stateHover

        # Add usmap to div
        $('#map').usmap {
          showLabels: true
          stateStyles: stateStyles
          stateHoverStyles: fill: colors.defaultFill
          stateHoverAnimation: 100
          stateSpecificStyles: stateStyleMap
          stateSpecificHoverStyles: stateHoverMap
          click: (event, data) ->
            if data.name in stateCodes
              window.location.href = edwareUtil.getBaseURL() + stateMapConfig.reportExtension + data.name
        }

        # get state label locations from json
        state_label_pos = stateMapConfig.state_pos
        
        #Removes the state codes that are added by usmap
        $('#map svg text tspan').each () ->
          if this.firstChild.data not in stateCodes or this.firstChild.data of state_label_pos
            this.firstChild.data = ''

        rem_x = []
        rem_y = []
        # Remove small state text boxes drawn by usmap.js
        $('#map svg rect').each () ->
          if $(this).attr('fill') == colors.usmapFill
            rem_x.push $(this).attr('x')
            rem_y.push $(this).attr('y')
            $(this).hide()

        # remove boxes on side of screen for old labels
        i = 0
        while i < rem_x.length
          x = rem_x[i]
          y = rem_y[i]
          $('#map svg text, #map svg rect').each () ->
            if $(this).attr('x') == x and $(this).attr('y') == y
              $(this).hide()
          ++i

        # get map svg object
        map_svg = $('#map svg')
        
        # add state codes and lines for small states
        for state_code, coord of state_label_pos
          if state_code in stateCodes
            st_txt = $(SVG('text')).attr(coord.name)
    
            st_span = $(SVG('tspan')).attr('dy', '5.682005882263184')  # dy moves Y coordinate down 
            st_span.append(state_code)
            st_txt.append(st_span)
            map_svg.append(st_txt)

            st_line = $(SVG('line'))
            st_line.attr(coord.line)
            map_svg.append(st_line)        

        edwareHeader.create(data, stateMapConfig)
        displayHome = edwareUtil.getDisplayBreadcrumbsHome data.user_info
        $('#breadcrumb').breadcrumbs(data.context, stateMapConfig.breadcrumb, displayHome)
