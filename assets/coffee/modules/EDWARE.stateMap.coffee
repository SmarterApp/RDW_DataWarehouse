require [
  'jquery'
  'raphael'
  'usmap'
  'edwareDataProxy'
  'edwareUtil'
  'edwareHeader'
  'edwareBreadcrumbs'
], ($, Raphael, usmap, edwareDataProxy, edwareUtil, edwareHeader, edwareBreadcrumbs) ->

  edwareDataProxy.getDataForReport('comparingPopulationsReport').done (reportConfig) ->
      options =
        method: 'POST'
      load = edwareDataProxy.getDatafromSource "/services/userinfo", options
      load.done (data) ->
        stateCodes = edwareUtil.getUserStateCode data.user_info
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
          if this.firstChild.data not in stateCodes
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

        $('#map svg').append('<text x="810" y="100" text-anchor="middle" stroke="none" fill="#ffffff" font-weight="300" stroke-width="0" font-size="13px">
<tspan dy="4.367921829223633">VT</tspan>
</text>')
        $('#map svg').append('<rect id="vt_box" x="800" y="75.03571428571429" width="26.571428571428573" height="19.928571428571427" r="3.9857142857142858" rx="3.9857142857142858" ry="3.9857142857142858" fill="#ffffff" stroke="#000" style="opacity: 0; cursor: pointer;" stroke-width="0" opacity="0">')
        # $('#map svg path').each ()

        edwareHeader.create(data, reportConfig)
        displayHome = edwareUtil.getDisplayBreadcrumbsHome data.user_info
        $('#breadcrumb').breadcrumbs(data.context, reportConfig.breadcrumb, displayHome)


