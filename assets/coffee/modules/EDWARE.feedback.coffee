define [
  'jquery'
  'mustache'
  "edwareDataProxy"
  "text!templates/feedback/feedback.html"
], ($, Mustache, edwareDataProxy, template) ->
   
  # Create Survey Monkey iframe based on the role, report.  Uses uid to append to the URL to identify the user that submits the survey
  renderFeedback = (role, uid, reportName) ->
    feedbackMapping = {}
    options =
      async: false
      method: "GET"
    
    edwareDataProxy.getDatafromSource "../data/feedback.json", options, (feedbackMapping) ->
      feedbackdata = {}
      if role of feedbackMapping
        if reportName of feedbackMapping[role]
          feedbackdata.param = feedbackMapping[role][reportName]
          feedbackdata.uid = uid
          
          # Render iframe with all other assets are loaded
          $(document).ready ->
            output = Mustache.to_html template, feedbackdata
            $("#surveyMonkeyInfo").html output

  renderFeedback: renderFeedback