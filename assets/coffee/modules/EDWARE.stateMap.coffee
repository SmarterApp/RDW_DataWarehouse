require [
  'jquery'
  'raphael'
  'usmap'
  'edwareDataProxy'
  'edwareUtil'
  'edwareHeader'
], ($, Raphael, usmap, edwareDataProxy, edwareUtil, edwareHeader) ->

  # TODO: remove/update "comparingPopulationReport"
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
        $('#titleString').append('<h2>Select State to start exploring Smarter Balanced test results</h2>')

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

        # Removes the state codes that are added by usmap
        $('#map svg text tspan').each () ->
          if this.firstChild.data not in stateCodes
            this.firstChild.data = ''

        # TODO: remove/update "individual_student_report"
        edwareHeader.create(data, reportConfig, "individual_student_report")

