require ['jquery', 'mustache', 'edwareDataProxy', 'text!templates/LandingPage.html'], ($, Mustache, edwareDataProxy, landingPageTemplate) ->
  
  #edwareDataProxy.getDatafromSource ['../data/common/en/labels.json', '../data/content/en/landingPage.json'], options, (data) ->
  edwareDataProxy.getDatafromSource '../data/common/en/labels.json', {}, (data) ->
    output = Mustache.to_html landingPageTemplate,
      labels: data.labels
    $('body').html output
  
