define [
  'jquery'
  'mustache'
  "cs!edwareDataProxy"
  "text!templates/feedback/feedback.html"
], ($, Mustache, edwareDataProxy, template) ->
    
  $.fn.renderFeedback = (role, reportName)->
    self = this
    feedbackMapping = {}
    options =
      async: false
      method: "GET"
    
    edwareDataProxy.getDatafromSource "../data/feedback.json", options, (feedbackMapping) ->
      feedbackdata = {}
      if role of feedbackMapping
        if reportName of feedbackMapping[role]
          feedbackdata.url = feedbackMapping[role][reportName]
      output = Mustache.to_html template, feedbackdata
      document.getElementById("survey").innerHTML = output
      #$('#content .surveyMonkeyPopup').load('https://www.surveymonkey.com/jsEmbed.aspx?sm=6JlFNpc_2fA9NB8dAfsEe3hg_3d_3d')
      $.getScript "https://www.surveymonkey.com/jsEmbed.aspx?sm=6JlFNpc_2fA9NB8dAfsEe3hg_3d_3d", (data, textStatus, jqxhr) ->
        console.log data #data returned
        console.log textStatus #success
        console.log jqxhr.status #200
        console.log "Load was performed."
