define [
  'jquery'
  'mustache'
  "cs!edwareDataProxy"
  "text!templates/feedback/feedback.html"
], ($, Mustache, edwareDataProxy, template) ->
    
  renderFeedback = (role, uid, reportName) ->
    self = this
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
          
          output = Mustache.to_html template, feedbackdata
          $("#surveyMonkeyInfo").html output
          
          # Survey monkey popup
          $("#feedback").popover
            html: true
            placement: "top"
            container: "footer"
            title: ->
                '<div class="pull-right"><button class="btn" id="close" type="button" onclick="$(&quot;#feedback&quot;).popover(&quot;hide&quot;);">Hide</button></div><div class="lead">Survery Monkey</div>'
            template: '<div class="popover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
            content: ->
              $(".surveyMonkeyPopup").html()

  renderFeedback: renderFeedback