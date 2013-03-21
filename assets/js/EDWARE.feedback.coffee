define [
  'jquery'
  "cs!edwareDataProxy"
], ($, edwareDataProxy) ->
    
  renderFeedback = (role, reportName)->
    self = this
    feedbackMapping = {}
    options =
      async: false
      method: "GET"
    
    edwareDataProxy.getDatafromSource "../data/feedback.json", options, (feedbackMapping) ->
      feedbackdata = {}
      if role of feedbackMapping
        if reportName of feedbackMapping[role]
          feedbackdata = feedbackMapping[role][reportName]
          
          iframeURL =  $("#surveyMonkeyInfo").find("iframe").attr("src")       
          iframeURL = iframeURL.split("?")[0]
          iframeURL = iframeURL + "?sm=" + feedbackdata         
          $("#surveyMonkeyInfo").find("iframe").attr("src", iframeURL)
          console.log $("#surveyMonkeyInfo").find("iframe").attr("src") 
          
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